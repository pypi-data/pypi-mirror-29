#!/usr/bin/env python
# whisker_autonomic_analysis/telemetry_means.py

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

from typing import List

from cardinal_pythonlib.reprfunc import simple_repr

from .cardiac_calcs import CardiacIndices
from .config import Config
from .heartbeat import Heartbeat, slice_telemetry, SliceBy
from .maths import dictminus, mean, ParamDict


class TelemetryMeans(object):
    PARAM_N_BEATS = "n_beats"
    PARAM_HR_MEAN_BPM = "HR"
    PARAM_SBP_MEAN_MMHG = "SBP"
    PARAM_DBP_MEAN_MMHG = "DBP"
    PARAM_MAP_MEAN_MMHG = "MAP"

    def __init__(self,
                 cfg: Config = None,
                 telemetry: List[Heartbeat] = None,
                 start_time_s: float = None,
                 end_time_s: float = None,
                 show_poincare_plot: bool = False,
                 show_filter_response: bool = False,
                 show_filtered_rsa: bool = False) -> None:
        # We allow blank construction for the subtraction operation.
        self.start_time_s = start_time_s
        self.end_time_s = end_time_s
        self.is_difference = False
        self.params = {}  # type: ParamDict

        if not telemetry:
            return

        # Slice, or use whole series:
        if start_time_s is not None and end_time_s is not None:
            assert start_time_s <= end_time_s
            # We will slice in different ways according to the values of
            # interest:
            sliced_by_r_time = slice_telemetry(
                telemetry,
                start_time_s=start_time_s,
                end_time_s=end_time_s,
                slice_by=SliceBy.R_TIME)
            sliced_by_sbp_time = slice_telemetry(
                telemetry,
                start_time_s=start_time_s,
                end_time_s=end_time_s,
                slice_by=SliceBy.SBP_TIME)
            sliced_by_dbp_time = slice_telemetry(
                telemetry,
                start_time_s=start_time_s,
                end_time_s=end_time_s,
                slice_by=SliceBy.DBP_TIME)
            hr_values_bpm = [x.hr_bpm for x in sliced_by_r_time]  # as per Laith's code  # noqa
            sbp_values_mmhg = [x.sbp_mmhg for x in sliced_by_sbp_time]  # as per Laith's code  # noqa
            dbp_values_mmhg = [x.dbp_mmhg for x in sliced_by_dbp_time]  # as per Laith's code  # noqa
            map_values_mmhg = [x.map_mmhg for x in sliced_by_sbp_time]  # as per Laith's code  # noqa
            ibi_values_ms = [x.rr_interval_ms for x in sliced_by_r_time]  # RNC
        elif start_time_s is not None or end_time_s is not None:
            raise ValueError("If you specify one of start_time_s or "
                             "end_time_s,  you must specify them both")
        else:
            assert telemetry is not None  # makes type checker happier
            hr_values_bpm = [x.hr_bpm for x in telemetry]
            sbp_values_mmhg = [x.sbp_mmhg for x in telemetry]
            dbp_values_mmhg = [x.dbp_mmhg for x in telemetry]
            map_values_mmhg = [x.map_mmhg for x in telemetry]
            ibi_values_ms = [x.rr_interval_ms for x in telemetry]

        # Calculate values
        self.params[self.PARAM_N_BEATS] = len(hr_values_bpm)
        self.params[self.PARAM_HR_MEAN_BPM] = mean(hr_values_bpm)
        self.params[self.PARAM_SBP_MEAN_MMHG] = mean(sbp_values_mmhg)
        self.params[self.PARAM_DBP_MEAN_MMHG] = mean(dbp_values_mmhg)
        self.params[self.PARAM_MAP_MEAN_MMHG] = mean(map_values_mmhg)

        if cfg.hrv:
            cardiac_indices = CardiacIndices(
                cfg=cfg,
                ibi_values_ms=ibi_values_ms,
                show_poincare_plot=show_poincare_plot,
                show_filter_response=show_filter_response,
                show_filtered_rsa=show_filtered_rsa
            )
            self.params.update(cardiac_indices.get_parameters())

    def __repr__(self) -> str:
        return simple_repr(self, [
            "is_difference",
            "start_time_s",
            "end_time_s",
            "params",
        ])

    def __sub__(self, other: 'TelemetryMeans') -> 'TelemetryMeans':
        # For calculating differences: self - other
        result = TelemetryMeans()
        result.params = dictminus(self.params, other.params)
        result.is_difference = True
        return result

    def get_parameters(self) -> ParamDict:
        return self.params

    def duration_s(self) -> float:
        if self.start_time_s is None or self.end_time_s is None:
            return 0.0
        return self.end_time_s - self.start_time_s
