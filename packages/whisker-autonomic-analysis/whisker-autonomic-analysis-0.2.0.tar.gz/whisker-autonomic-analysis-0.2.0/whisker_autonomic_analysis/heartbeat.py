#!/usr/bin/env python
# whisker_autonomic_analysis/heartbeat.py

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
from typing import List

from cardinal_pythonlib.reprfunc import simple_repr

from .config import Config
from .maths import hr_bpm_from_rr_ms

log = logging.getLogger(__name__)


# =============================================================================
# Heartbeat object, derived from Spike "peak" file format
# =============================================================================

class Heartbeat(object):
    def __init__(self,
                 cfg: Config,
                 r_time_s: float,
                 rr_interval_ms: float,
                 hr_bpm: float,
                 sbp_time_s: float,
                 sbp_mmhg: float,
                 dbp_time_s: float,
                 dbp_mmhg: float) -> None:
        """
        Class to store telemetry information, representing one row of a Spike
        "peak" file.

        :param r_time_s: time (R wave?) at which heart rate (HR) measured (s)
            ... presumably estimated somehow, since the ultimate source is a
            continuous BP trace, without ECG data.
        :param rr_interval_ms: R-R interval (= reciprocal of HR) (ms)
            a.k.a. interbeat interval (IBI)
        :param hr_bpm: HR in beats per minute
        :param sbp_time_s: time at which systolic blood pressure (SBP) measured
            (s)
        :param sbp_mmhg: SBP in millimetres of mercury
        :param dbp_time_s: time at which diastolic BP (DBP) measured (s)
        :param dbp_mmhg: DBP in millimetres of mercury

        Is the RR interval from the preceding beat, or to the next beat?
        Empirically, we check the meaning of RR interval as follows:
        (A) r_time[2] = r_time[1] + rr_interval[1]
        (B) r_time[1] = r_time[2] - rr_interval[2]

        Once three outliers are removed from the demo data set (see
        checking_rr_calcs.ods), there is nothing in it! They seem equally
        accurate (SSE_A = 0.00751689; SSE_B = 0.00758641).
        """
        self.r_time_s = r_time_s
        self.rr_interval_ms = rr_interval_ms
        self.hr_bpm = hr_bpm
        self.sbp_time_s = sbp_time_s
        self.sbp_mmhg = sbp_mmhg
        self.sbp_mmhg = sbp_mmhg
        self.dbp_time_s = dbp_time_s
        self.dbp_mmhg = dbp_mmhg
        assert r_time_s >= 0
        assert sbp_time_s >= 0
        assert dbp_time_s >= 0
        # noinspection PyTypeChecker
        assert r_time_s <= sbp_time_s < dbp_time_s, repr(self)
        # noinspection PyTypeChecker
        assert cfg.valid_hr_min_bpm <= hr_bpm <= cfg.valid_hr_max_bpm, repr(self)  # noqa
        # noinspection PyTypeChecker
        assert cfg.valid_bp_min_mmhg <= sbp_mmhg <= cfg.valid_bp_max_mmhg, repr(self)  # noqa
        # noinspection PyTypeChecker
        assert cfg.valid_bp_min_mmhg <= dbp_mmhg <= cfg.valid_bp_max_mmhg, repr(self)  # noqa
        recalc_hr = hr_bpm_from_rr_ms(rr_interval_ms)
        if abs(hr_bpm - recalc_hr) > cfg.valid_max_hr_error_bpm:
            raise ValueError(
                "hr_bpm ({}) too different from HR calculated from "
                "rr_interval_ms ({}) of {}".format(
                    hr_bpm, rr_interval_ms, recalc_hr))

    def __repr__(self) -> str:
        return simple_repr(self, ["r_time_s", "rr_interval_ms", "hr_bpm",
                                  "sbp_time_s", "sbp_mmhg",
                                  "dbp_time_s", "dbp_mmhg"])

    # Method A:
    def calc_next_beat_r_time_s(self) -> float:
        return self.r_time_s + (self.rr_interval_ms / 1000)

    # Method B:
    def calc_prev_beat_r_time_s(self) -> float:
        return self.r_time_s - (self.rr_interval_ms / 1000)

    @property
    def pulse_pressure_mmhg(self) -> float:
        return self.sbp_mmhg - self.dbp_mmhg

    @property
    def map_mmhg(self) -> float:
        """
        Calculates mean arterial pressure (MAP) as DBP + (1/3) * pulse pressure
        """
        return self.dbp_mmhg + (self.pulse_pressure_mmhg / 3)

    @property
    def rr_interval_s(self) -> float:
        return self.rr_interval_ms / 1000


# =============================================================================
# Telemetry aggregation and calculation
# =============================================================================

class SliceBy(object):
    R_TIME = 'r_time'
    SBP_TIME = 'sbp_time'
    DBP_TIME = 'dbp_time'


def slice_telemetry(telemetry: List[Heartbeat],
                    start_time_s: float,
                    end_time_s: float,
                    slice_by: str) -> List[Heartbeat]:
    """
    Chops up a telemetry list such that all heartbeats have their time
    within the range defined by [start_time_s, end_time_s), i.e. inclusive
    for start and exclusive for end (as per Laith).

    However, there are several times associated with each heartbeat.
    Which "time" should be used? That's determined by slice_by, which can take
    values:
        'r_time'
        'sbp_time'
        'dbp_time'
    """
    # Resist the temptation to provide a default to slice_by;
    # we want users to be very clear about what they're slicing on.
    if start_time_s >= end_time_s:
        log.debug("slice_telemetry: returning [] because start_time_s ({}) >= "
                  "end_time_s ({})".format(start_time_s, end_time_s))
        return []
    if slice_by == SliceBy.R_TIME:
        # noinspection PyTypeChecker
        return [x for x in telemetry
                if start_time_s <= x.r_time_s < end_time_s]
    elif slice_by == SliceBy.SBP_TIME:
        # noinspection PyTypeChecker
        return [x for x in telemetry
                if start_time_s <= x.sbp_time_s < end_time_s]
    elif slice_by == SliceBy.DBP_TIME:
        # noinspection PyTypeChecker
        return [x for x in telemetry
                if start_time_s <= x.dbp_time_s < end_time_s]
    else:
        raise ValueError("Invalid slice_by parameter")
