#!/usr/bin/env python
# whisker_autonomic_analysis/trial_timing.py

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
import math
import pprint
from typing import Optional

from cardinal_pythonlib.reprfunc import simple_repr

from .session_definition import SessionDefinition
from .telemetry_means import TelemetryMeans

log = logging.getLogger(__name__)


# =============================================================================
# Processing behavioural task data re CS/US timings
# =============================================================================

class TrialTiming(object):
    def __init__(self,
                 session_definition: SessionDefinition,
                 trial_number: int,
                 trial_start: float,
                 baseline_start_time_s: float,
                 cs_on_time_s: float,
                 cs_off_time_s: float,
                 us_on_time_s: float,
                 us_off_time_s: float,
                 iti_end: Optional[float]) -> None:
        self.session_definition = session_definition
        self.trial_number = trial_number
        self.trial_start = trial_start
        self.baseline_start_time_s = baseline_start_time_s
        self.cs_on_time_s = cs_on_time_s
        self.cs_off_time_s = cs_off_time_s
        self.us_on_time_s = us_on_time_s
        self.us_off_time_s = us_off_time_s
        self.iti_end = iti_end
        # Some checks:
        try:
            assert session_definition is not None
            assert trial_number >= 0
            assert baseline_start_time_s >= 0
            assert cs_on_time_s >= baseline_start_time_s
            assert cs_off_time_s >= cs_on_time_s
            # assert us_on_time_s >= cs_off_time_s  # NO, this can be false happily (CS can co-terminate with US).  # noqa
            assert us_off_time_s >= us_on_time_s
        except AssertionError:
            log.critical(pprint.pformat({
                'session_definition': session_definition,
                'trial_number': trial_number,
                'baseline_start_time_s': baseline_start_time_s,
                'cs_on_time_s': cs_on_time_s,
                'cs_off_time_s': cs_off_time_s,
                'us_on_time_s': us_on_time_s,
                'us_off_time_s': us_off_time_s,
            }))
            raise

    def __repr__(self) -> str:
        return simple_repr(self, ["trial_number", "baseline_start_time_s",
                                  "cs_on_time_s", "cs_off_time_s",
                                  "us_on_time_s", "us_off_time_s"])

    def get_baseline_start_time_s(self) -> float:
        return self.baseline_start_time_s

    def get_baseline_end_time_s(self) -> float:
        """Baseline ends when CS starts. (Note sanity check in constructor.)"""
        return self.cs_on_time_s

    def get_cs_alone_start_time_s(self) -> float:
        return self.cs_on_time_s

    def get_cs_alone_end_time_s(self) -> float:
        """
        The "CS alone" period ends either when the CS ends, or when the US
        starts (in case we have an overlap: CS -> CS+US).
        As a sanity check, we also say that the CS can't end before it
        starts.
        """
        return max(self.cs_on_time_s,
                   min(self.cs_off_time_s,
                       self.us_on_time_s))

    def get_us_start_time_s(self) -> float:
        return self.us_on_time_s

    def get_us_end_time_s(self) -> float:
        return self.us_off_time_s

    def get_chunk_duration_s(self) -> float:
        return self.session_definition.chunk_duration_s

    def _get_n_chunks(self, start_time_s, end_time_s) -> int:
        overall_time = max(0.0, end_time_s - start_time_s)
        chunk_time = self.get_chunk_duration_s()
        n_chunks = math.ceil(overall_time / chunk_time)  # type: int
        return n_chunks

    def get_n_baseline_chunks(self) -> int:
        return self._get_n_chunks(self.get_baseline_start_time_s(),
                                  self.get_baseline_end_time_s())

    def get_n_cs_alone_chunks(self) -> int:
        return self._get_n_chunks(self.get_cs_alone_start_time_s(),
                                  self.get_cs_alone_end_time_s())

    def get_n_us_chunks(self) -> int:
        return self._get_n_chunks(self.get_us_start_time_s(),
                                  self.get_us_end_time_s())

    def is_full_chunk(self, tm: TelemetryMeans):
        return tm.duration_s() >= self.get_chunk_duration_s()
