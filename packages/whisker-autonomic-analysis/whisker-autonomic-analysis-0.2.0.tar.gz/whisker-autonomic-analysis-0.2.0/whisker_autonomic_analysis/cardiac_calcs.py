#!/usr/bin/env python
# whisker_autonomic_analysis/cardiac_calcs.py

"""
===============================================================================
    Copyright (C) 2017-2018 Rudolf Cardinal (rudolf@pobox.com).

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
===============================================================================
"""

import logging
import os
import pprint
import re
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional

from cardinal_pythonlib.dicts import prefix_dict_keys, rename_keys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection

from .config import Config
from .maths import (
    coordinates_from_x_y,
    hr_bpm_from_rr_ms,
    ParamDict,
    rms,
    rotate_coordinates,
    rotation_matrix,
    x_y_from_coordinates,
)
from .timeseries import (
    filter_time_series,
    time_series_from_ibi,
)

log = logging.getLogger(__name__)
PlotType = PathCollection  # in case we return plots, for the type checker


# =============================================================================
# Support functions
# =============================================================================

def log10(x: Optional[float]) -> Optional[float]:
    if x is not None and x > 0:
        return np.log10(x)
    return None


def ln_var(x: Optional[np.array]) -> Optional[float]:
    if x is None:
        return None
    variance = np.var(x)
    if variance == 0:
        return None
    return np.log(variance)


def pnn(abs_nn_diffs: np.array, over_length_ms: int) -> Optional[float]:
    """
    e.g. PNN50: Proportion of the consecutive (absolute) IBI differences
    greater than 50 msec [3]
    """
    n_ibi_diffs = len(abs_nn_diffs)
    if n_ibi_diffs == 0:
        return None
    n_ibi_diffs_over = len([d for d in abs_nn_diffs
                            if d > over_length_ms])
    return n_ibi_diffs_over / n_ibi_diffs


# =============================================================================
# External HRV analysis using HRV toolkit
# =============================================================================
# - Note: Kubios HRV is no good for this sort of thing as it doesn't seem to
#   have a command-line interface.

GET_HRV_OUTPUT = re.compile(r'(\S+)\s*=\s*(-?\d+\.?\d*)')


def get_hrv_toolkit_params(
        cfg: Config,
        ibi_values_ms: List[float],
        debug_print_file: bool = False,
        debug_wait_for_user: bool = False,
        debug_show_stdout: bool = False) -> Dict[str, float]:
    """
    Example output from get_hrv:

/tmp/tmp2yvd0lpa/tmp03tr_euy :
NN/RR    = 0.999579
AVNN     = 0.18922
SDNN     = 0.0212386
SDANN    = 0.017645
SDNNIDX  = 0.0181617
rMSSD    = 0.00863746
pNN50    = 0.00210704
    """
    if not cfg.hrvtk_get_hrv_filename:
        return {}
    if cfg.hrvtk_cd_to_get_hrv:
        hrvtk_dir = os.path.dirname(cfg.hrvtk_get_hrv_filename)
        log.debug("Changing directory to " + repr(hrvtk_dir))
        os.chdir(hrvtk_dir)
    with tempfile.NamedTemporaryFile(mode='wt', dir=cfg.tempdir.name,
                                     delete=False) as rr_file:
        rr_filename = rr_file.name
        log.debug("Writing RR data to " + repr(rr_filename))
        for ibi_ms in ibi_values_ms:
            print(ibi_ms, file=rr_file)
    # The file is now closed, but exists on disk, and we have its name.
    # Since it was created in our temporary directory, it will be cleaned up
    # when the program exits.
    if debug_print_file:
        with open(rr_filename) as f:
            for line in f:  # http://stackoverflow.com/questions/17246260
                print(line, end='')
    if debug_wait_for_user:
        input("Press Enter to continue...")
    cmdargs = [
        cfg.hrvtk_get_hrv_filename,
        '-m',  # RR intervals in ms, not s
        '-R', rr_filename,
    ]
    process = subprocess.Popen(cmdargs, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout_bin, stderr_bin = process.communicate()
    stdout = stdout_bin.decode(sys.getdefaultencoding()) if stdout_bin else ''
    stderr = stderr_bin.decode(sys.getdefaultencoding()) if stderr_bin else ''
    if stderr:
        log.warning("Error(s) from the HRV Toolkit 'get_hrv' tool:")
        log.warning(stderr)
    if debug_show_stdout:
        log.debug("Output from get_hrv:\n" + stdout)
    results = {}  # type: Dict[str, float]
    for m in GET_HRV_OUTPUT.finditer(stdout):
        try:
            param = m.group(1)
            value = float(m.group(2))
            results[param] = value
        except (TypeError, ValueError):
            pass
    log.debug("get_hrv reported: " + repr(results))
    return results


# =============================================================================
# Poincaré plot, for Toichi CSI/CVI indices
# =============================================================================

class PoincarePlot(object):
    """
    Toichi (1997) [4] calls this a Lorenz plot, but Lorenz doesn't use it in
    the 1963 paper cited [5]; it's probably a Poincaré plot [6].
    """
    ROTATE_ANTICLOCKWISE_45 = rotation_matrix(45)
    ROTATE_CLOCKWISE_45 = rotation_matrix(-45)

    def __init__(self, intervals: np.ndarray, debug: bool = False) -> None:
        self.intervals = intervals
        self.x = intervals[:-1]  # all but the last
        self.y = intervals[1:]  # all but the first
        self.sd_longit = None
        self.sd_transverse = None
        self.toichi_l = None
        self.toichi_t = None
        self.l_line_coords = None
        self.t_line_coords = None

        if len(intervals) > 1:
            coords = coordinates_from_x_y(self.x, self.y)
            rotated_coords = rotate_coordinates(coords,
                                                self.ROTATE_ANTICLOCKWISE_45)
            transverse, longit = x_y_from_coordinates(rotated_coords)
            self.sd_longit = np.std(longit)  # type: float
            # ... this is called "SD2" by Kubios HRV
            self.sd_transverse = np.std(transverse)  # type: float
            # ... this is called "SD1" by Kubios HRV

            self.toichi_l = 4 * self.sd_longit  # [4]
            self.toichi_t = 4 * self.sd_transverse  # [4]

            mean_longit = np.mean(longit)
            mean_transverse = np.mean(transverse)
            rotated_l_coords = np.array([
                [mean_transverse, mean_longit - self.toichi_l / 2],
                [mean_transverse, mean_longit + self.toichi_l / 2]
            ])
            rotated_t_coords = np.array([
                [mean_transverse - self.toichi_t / 2, mean_longit],
                [mean_transverse + self.toichi_t / 2, mean_longit]
            ])
            self.l_line_coords = rotate_coordinates(rotated_l_coords,
                                                    self.ROTATE_CLOCKWISE_45)
            self.t_line_coords = rotate_coordinates(rotated_t_coords,
                                                    self.ROTATE_CLOCKWISE_45)

            if debug:
                log.debug("PoincarePlot.__init__:\n" + pprint.pformat({
                    'longit': longit,
                    'transverse': transverse,
                    'mean_longit': mean_longit,
                    'mean_transverse': mean_transverse,
                    'self.sd_longit': self.sd_longit,
                    'self.sd_transverse': self.sd_transverse,
                    'rotated_l_coords': rotated_l_coords,
                    'rotated_t_coords': rotated_t_coords,
                    'self.l_coords': self.l_line_coords,
                    'self.t_coords': self.t_line_coords,
                    'coords': coords,
                    'rotated_coords': rotated_coords,
                    'self.x': self.x,
                    'self.y': self.y,
                }))

    @property
    def toichi_l_over_t(self) -> Optional[float]:
        if self.toichi_l is None or self.toichi_t is None or self.toichi_t == 0:
            return None
        return self.toichi_l / self.toichi_t

    @property
    def toichi_l_times_t(self) -> Optional[float]:
        if self.toichi_l is None or self.toichi_t is None:
            return None
        return self.toichi_l * self.toichi_t

    @property
    def sd1(self) -> float:
        # sd_transverse is called SD1 by Kubios HRV
        return self.sd_transverse

    @property
    def sd2(self) -> float:
        # sd_longit is called SD2 by Kubios HRV
        return self.sd_longit

    def plot(self) -> None:
        if self.intervals is None or len(self.intervals) == 0:
            return
        fig = plt.figure()

        tacho_x = list(range(len(self.intervals)))
        tacho_y = self.intervals
        tacho_ax = fig.add_subplot(3, 1, 1)
        tacho_ax.set_title("IBI by beat")
        tacho_ax.set_xlabel("Beat number")
        tacho_ax.set_ylabel("Interbeat_interval (ms)")
        tacho_ax.plot(tacho_x, tacho_y, 'k-')
        tacho_ax.plot(tacho_x, tacho_y, 'ro')

        rate_x = list(range(len(self.intervals)))
        rate_y = hr_bpm_from_rr_ms(self.intervals)
        rate_ax = fig.add_subplot(3, 1, 2)
        rate_ax.set_title("Calculated rate by beat")
        rate_ax.set_xlabel("Beat number")
        rate_ax.set_ylabel("HR (bpm)")
        rate_ax.plot(rate_x, rate_y, 'k-')
        rate_ax.plot(rate_x, rate_y, 'ro')

        poincare_x = self.intervals[:-1]  # all but the last
        poincare_y = self.intervals[1:]  # all but the first
        poincare_ax = fig.add_subplot(3, 1, 3)
        poincare_ax.set_title("Poincaré plot")
        poincare_ax.set_xlabel("Interbeat_interval[k] (ms)")
        poincare_ax.set_ylabel("Interbeat_interval[k+1] (ms)")
        poincare_ax.plot(poincare_x, poincare_y, 'ro')

        l_x, l_y = x_y_from_coordinates(self.l_line_coords)
        t_x, t_y = x_y_from_coordinates(self.t_line_coords)
        poincare_ax.plot(l_x, l_y, 'k-')
        poincare_ax.plot(t_x, t_y, 'k-')
        poincare_ax.text(l_x[1], l_y[1], "L")
        poincare_ax.text(t_x[1], t_y[1], "T")

        fig.gca().set_aspect('equal', adjustable='box')
        # fig.tight_layout()

        plt.show()


# =============================================================================
# CardiacIndices
# =============================================================================

class CardiacIndices(object):
    PARAM_CSI = "CSI"
    PARAM_CVI_LOG10_MS = "CVI_log10_ms"
    PARAM_HRV_LN_MS2 = "HRV_ln_ms2"
    PARAM_IBI_MEAN_MS = "IBI_mean_ms"
    PARAM_MEAN_HR_FROM_IBI_BPM = "HR_mean_from_IBIs_bpm"
    PARAM_MSD_MS = "MSD_ms"
    PARAM_N_IBI = "n_IBI"
    PARAM_PNN50 = "PNN50"
    PARAM_RMSSD_MS = "RMSSD_ms"
    PARAM_RSA_LN_MS2 = "RSA_ln_ms2"
    PARAM_SDNN_MS = "SDNN_ms"
    PARAM_TOICHI_KUBIOS_SD1 = "Toichi_Kubios_SD1_T_ms"
    PARAM_TOICHI_KUBIOS_SD2 = "Toichi_Kubios_SD2_L_ms"
    PARAM_TOICHI_L_MS = "Toichi_L_ms"
    PARAM_TOICHI_T_MS = "Toichi_T_ms"

    HRV_TOOLKIT_PREFIX = "HRVToolkit_"
    # For details see [10]:
    HRV_TOOLKIT_RENAMES = {
        'rMSSD': 'RMSSD_s',
        # ... Square root of the mean of the squares of differences between
        #     adjacent NN intervals

        # 'NN/RR'  # unchanged
        # ... "NN/RR is the fraction of total RR intervals that are classified
        #     as normal-to-normal (NN) intervals and included in the
        #     calculation of HRV statistics. This ratio can be used as a
        #     measure of data reliability. For example, if the NN/RR ratio is
        #     less than 0.8, fewer than 80% of the RR intervals are classified
        #     as NN intervals, and the results will be somewhat unreliable."
        #     [10]

        # 'pNN50'  # unchanged
        # ... Percentage of differences between adjacent NN intervals that are
        #     greater than 50 ms; a member of the larger pNNx family

        'AVNN': 'AVNN_s',  # average of all NN intervals

        'SDNN': 'SDNN_s',  # SD of all NN intervals

        'SDANN': 'SDANN_s',
        # ... SD of averages of NN intervals in all 5-minute segments of a 24-h
        #     recording

        'SDNNIDX': 'SDNNIDX_s',
        # ... Mean of the SDs of NN intervals in all 5-minute segments of a
        #     24-h recording
    }

    def __init__(self,
                 cfg: Config,
                 ibi_values_ms: List[float],
                 show_poincare_plot: bool = False,
                 show_filter_response: bool = False,
                 show_filtered_rsa: bool = False) -> None:
        self.params = {}  # type: ParamDict
        self.is_difference = False

        if not ibi_values_ms:
            return
        assert None not in ibi_values_ms

        if cfg.hrv_builtin:
            # =================================================================
            # Our own HRV calculations
            # =================================================================
            nn = np.array(ibi_values_ms, dtype=float)
            # ... beat-to-beat intervals are often called NN intervals [1, 2],
            # and it's a short name.
            nn_diffs = np.diff(nn, n=1)

            poincare_plot = PoincarePlot(nn)
            if show_poincare_plot:
                poincare_plot.plot()

            # -----------------------------------------------------------------
            # Misc
            # -----------------------------------------------------------------

            # Mean interbeat interval [2, 3]
            self.params[self.PARAM_IBI_MEAN_MS] = np.mean(nn)  # type: float

            # Mean heart rate (recalculated from IBIs) [2, 3]
            self.params[self.PARAM_MEAN_HR_FROM_IBI_BPM] = \
                np.mean(hr_bpm_from_rr_ms(nn))

            # Toichi: Cardiac Sympathetic Index [4]
            self.params[self.PARAM_CSI] = poincare_plot.toichi_l_over_t  # [4, p82]  # noqa

            # Toichi L: Length of longitudinal axis [4]
            self.params[self.PARAM_TOICHI_L_MS] = poincare_plot.toichi_l
            # and corresponding SD:
            self.params[self.PARAM_TOICHI_KUBIOS_SD2] = poincare_plot.sd2

            # Toichi T: Length of transverse axis [4]
            self.params[self.PARAM_TOICHI_T_MS] = poincare_plot.toichi_t
            # and corresponding SD:
            self.params[self.PARAM_TOICHI_KUBIOS_SD1] = poincare_plot.sd1

            # Number of interbeat intervals [3]
            self.params[self.PARAM_N_IBI] = len(nn)

            # -----------------------------------------------------------------
            # Measures of heart rate variability (both sympathetic and
            # parasympathetic influences) [3]
            # -----------------------------------------------------------------

            # Standard deviation of IBIs [2, 3]
            self.params[self.PARAM_SDNN_MS] = np.std(nn)  # type: float

            # Root-mean-square of differences between IBIs [2, 3]
            self.params[self.PARAM_RMSSD_MS] = rms(nn_diffs)

            abs_nn_diffs = np.abs(nn_diffs)

            # MSD: Mean of the absolute value of consecutive IBI differences [3]
            self.params[self.PARAM_MSD_MS] = np.mean(abs_nn_diffs)  # type: float  # noqa

            # Heart rate variability
            # - affected by SNS & PNS
            # - operationalized as natural log of variance of IBI series [2, 3]
            self.params[self.PARAM_HRV_LN_MS2] = ln_var(nn)

            # -----------------------------------------------------------------
            # Measures of respiratory sinus arrhythmia [3]
            # ... which is not the same as vagal tone [7]
            # -----------------------------------------------------------------

            # PNN50: Proportion of the consecutive (absolute) IBI differences
            # greater than 50 msec [3]
            self.params[self.PARAM_PNN50] = pnn(abs_nn_diffs,
                                                over_length_ms=50)

            # CVI: Toichi Cardiac Vagal Index
            self.params[self.PARAM_CVI_LOG10_MS] = (
                log10(poincare_plot.toichi_l_times_t)  # [4, p. 81]
            )

            # LogRSA: Natural log of variance of filtered (.12-.40 Hz) IBI
            # series [2, 9]
            ts = time_series_from_ibi(ibi_ms=nn,
                                      frequency_hz=cfg.hrv_resample_freq_hz)
            filtered = filter_time_series(
                time_series=ts,
                numtaps=cfg.rsa_numtaps,
                low_cutoff_hz=cfg.rsa_low_cutoff_hz,
                high_cutoff_hz=cfg.rsa_high_cutoff_hz,
                sampling_freq_hz=cfg.hrv_resample_freq_hz,
                show_filter_response=show_filter_response,
                show_plot=show_filtered_rsa
            )
            _, fil_y = x_y_from_coordinates(filtered)
            self.params[self.PARAM_RSA_LN_MS2] = ln_var(fil_y)  # units: ln(ms^2)  # noqa

        # =====================================================================
        # Add in external tool results
        # =====================================================================

        hrvtk_params = get_hrv_toolkit_params(cfg=cfg,
                                              ibi_values_ms=ibi_values_ms)
        hrvtk_params = rename_keys(hrvtk_params, self.HRV_TOOLKIT_RENAMES)
        hrvtk_params = prefix_dict_keys(hrvtk_params, self.HRV_TOOLKIT_PREFIX)
        self.params.update(hrvtk_params)

    def __repr__(self) -> str:
        return "CardiacIndices({})".format(self.params)

    def get_parameters(self) -> ParamDict:
        return self.params
