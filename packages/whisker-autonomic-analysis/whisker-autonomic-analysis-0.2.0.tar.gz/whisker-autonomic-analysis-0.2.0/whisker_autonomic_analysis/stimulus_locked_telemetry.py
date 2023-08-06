#!/usr/bin/env python
# whisker_autonomic_analysis/stimulus_locked_telemetry.py

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
from typing import Generator, List, Optional

from cardinal_pythonlib.reprfunc import auto_repr

from .config import Config
from .heartbeat import Heartbeat
from .maths import to_db_float
from .telemetry_means import TelemetryMeans
from .trial_telemetry_record import TrialTelemetryRecord
from .trial_timing import TrialTiming

log = logging.getLogger(__name__)


class StimulusLockedTelemetry(object):
    def __init__(self,
                 telemetry: List[Heartbeat],
                 trial_timing: TrialTiming,
                 cfg: Config,
                 peak_filename: str) -> None:
        # This function is a bit inelegant; it presupposes a certain way of
        # dividing up time. This is the bit of this program that is most tied
        # to a specific behavioural task.
        #
        # The code follows Laith's; the only generalization is chunk_s being
        # a variable (and that we don't do the same thing multiple times to
        # measure multiple variables).
        #
        # Note that the subtraction measures are redundant (they could be
        # calculated by the user from the other data) but are provided as
        # a convenience, and marked as being "difference" data in the database.
        #
        # WE ASSUME that the baseline runs from the baseline start time to the
        # CS onset time.
        #
        # The baseline and CS are sliced into two;
        #   (1) start -> (end - chunk_duration)
        #   (2) (end - chunk_duration) -> end

        self.trial_timing = trial_timing
        self.peak_filename = peak_filename
        self.phases = {}  # Dict[str, TelemetryMeans]
        # Everything is split into chunks, defined by the chunk length.
        chunk_dur_s = trial_timing.get_chunk_duration_s()

        def add_directly(phase: str, tm: TelemetryMeans) -> None:
            self.phases[phase] = tm

        def add_phase(phase: str,
                      start_time_s: float,
                      end_time_s: float) -> TelemetryMeans:
            tm = TelemetryMeans(cfg=cfg,
                                telemetry=telemetry,
                                start_time_s=start_time_s,
                                end_time_s=end_time_s)
            add_directly(phase, tm)
            return tm

        def chunky(prefix: str,
                   start_time_s: float,
                   end_time_s: float,
                   n_chunks: int) -> List[TelemetryMeans]:
            chunklist = []  # type: List[TelemetryMeans]
            for chunk_index in range(n_chunks):
                chunk_num = chunk_index + 1
                chunklist.append(add_phase(
                    "{}{}".format(prefix, chunk_num),
                    start_time_s=min(
                        start_time_s + chunk_index * chunk_dur_s,
                        end_time_s
                    ),
                    end_time_s=min(
                        start_time_s + (chunk_index + 1) * chunk_dur_s,
                        end_time_s
                    )
                ))
            return chunklist

        def last_complete_chunk(
                chunklist: List[TelemetryMeans]) -> Optional[TelemetryMeans]:
            for chunk in reversed(chunklist):
                if trial_timing.is_full_chunk(chunk):
                    return chunk
            return None

        def compare_chunks(prefix: str,
                           chunks_of_interest: List[TelemetryMeans],
                           comparator_chunks: List[TelemetryMeans]) -> None:
            # We compare each of the chunks_of_interest, as long as they're
            # complete, to the last full-length chunk of comparator_chunks.
            refchunk = last_complete_chunk(comparator_chunks)
            if not refchunk:
                log.warning(
                    "No suitable reference chunk for comparison (#comparators "
                    "= {})".format(len(comparator_chunks)))
                return
            for chunk_index in range(len(chunks_of_interest)):
                chunk_num = chunk_index + 1
                chunk_of_interest = chunks_of_interest[chunk_index]
                if not trial_timing.is_full_chunk(chunk_of_interest):
                    continue  # too short
                add_directly(
                    "{}{}".format(prefix, chunk_num),
                    chunk_of_interest - refchunk
                )

        baseline_start_time_s = trial_timing.get_baseline_start_time_s()
        baseline_end_time_s = trial_timing.get_baseline_end_time_s()
        cs_alone_start_time_s = trial_timing.get_cs_alone_start_time_s()
        cs_alone_end_time_s = trial_timing.get_cs_alone_end_time_s()
        us_start_time_s = trial_timing.get_us_start_time_s()
        us_end_time_s = trial_timing.get_us_end_time_s()

        # The simple things: entire baseline/CS alone/US periods.
        baseline = add_phase('baseline',
                             start_time_s=baseline_start_time_s,
                             end_time_s=baseline_end_time_s)
        cs_alone = add_phase('CS_alone',
                             start_time_s=cs_alone_start_time_s,
                             end_time_s=cs_alone_end_time_s)
        us = add_phase('US',
                       start_time_s=us_start_time_s,
                       end_time_s=us_end_time_s)

        # Comparison of entire periods
        add_directly('CS_directed', cs_alone - baseline)
        add_directly('US_directed', us - cs_alone)

        # The chunks
        baseline_chunks = chunky("baseline_",
                                 baseline_start_time_s,
                                 baseline_end_time_s,
                                 trial_timing.get_n_baseline_chunks())
        cs_alone_chunks = chunky("CS_alone_",
                                 cs_alone_start_time_s,
                                 cs_alone_end_time_s,
                                 trial_timing.get_n_cs_alone_chunks())
        us_chunks = chunky("US_",
                           us_start_time_s,
                           us_end_time_s,
                           trial_timing.get_n_us_chunks())

        # The comparisons of chunks to each other.
        log.debug("Comparing CS-alone chunks to last complete baseline chunk")
        compare_chunks("CS_directed_", cs_alone_chunks, baseline_chunks)
        log.debug("Comparing US chunks to last complete CS-alone chunk")
        compare_chunks("US_directed_", us_chunks, cs_alone_chunks)

    def __repr__(self) -> str:
        return auto_repr(self)

    def gen_trial_telemetry_records(self) -> Generator[TrialTelemetryRecord,
                                                       None, None]:
        tt = self.trial_timing
        sd = tt.session_definition
        for phase_tm in self.phases.items():
            # Process tuple, then split, so the type checker knows...
            phase = phase_tm[0]  # type: str
            tm = phase_tm[1]  # type: TelemetryMeans
            is_difference = tm.is_difference
            for ap, value in tm.get_parameters().items():
                yield TrialTelemetryRecord(
                    date_time=sd.date_time,
                    subject=sd.subject,
                    box=sd.box,

                    trial=tt.trial_number,
                    peak_filename=self.peak_filename,
                    phase=phase,

                    start_time_s=tm.start_time_s,
                    end_time_s=tm.end_time_s,
                    autonomic_parameter=ap,
                    parameter_value=to_db_float(value),
                    is_difference=is_difference,
                )
