#!/usr/bin/env python
# whisker_autonomic_analysis/spike_file.py

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

import itertools
import logging
from typing import Generator, List

from .config import Config
from .heartbeat import Heartbeat
from .telemetry_means import TelemetryMeans

log = logging.getLogger(__name__)


SPIKE_FIRSTLINES_RRINT_MS = [
    "#  time\t   RR-Int\t Heart Rate\t   time\t  Systole\t   time\t  Diastole",
]
SPIKE_FIRSTLINES_RRINT_SEC = [
    'Time\tRRint\tHeartrate\tTime\tSystolic\tTime\tDiastolic',
]


# =============================================================================
# Spike "peak" file format
# =============================================================================

def gen_telemetry(cfg: Config,
                  filename: str,
                  skip_initial_n_lines: int = 2,
                  end_time_marker_s: float = 10000) \
        -> Generator[Heartbeat, None, None]:
    """
    Generates TelemetryDatum items from a Spike peak file.

    :param cfg: Config object
    :param filename: filename
    :param skip_initial_n_lines: number of header lines to skip
    :param end_time_marker_s: when the time is this value, that's the
        end-of-file marker (accompanied by zero values in all other columns).
    """
    log.info("Reading Spike peak data from " + repr(filename))
    with open(filename, "r") as f:
        # http://stackoverflow.com/questions/2970780/pythonic-way-to-do-something-n-times-without-an-index-variable  # noqa
        firstline = None
        for _ in itertools.repeat(None, skip_initial_n_lines):
            if firstline is None:
                firstline = f.readline().strip()
            else:
                next(f)

        # 2018-08-03: deal with variation in Spike peak file units for the
        # RR interval (looks like two different Spike programs being run
        # contemporaneously!)
        if firstline in SPIKE_FIRSTLINES_RRINT_MS:
            log.info("First line suggests RR interval in milliseconds "
                     "(through nasty code)")
            spike_rrint_in_ms = True
            expected_num_columns = 8  # always has a null "0" column at the end
            col_7_always_zero = True
        elif firstline in SPIKE_FIRSTLINES_RRINT_SEC:
            log.info("First line suggests RR interval in seconds "
                     "(through nasty code)")
            spike_rrint_in_ms = False
            expected_num_columns = 7
            col_7_always_zero = False
        else:
            errmsg = (
                "Can't be sure of the units of time being used by "
                "the Spike peak file for its R-R intervals; aborting. First "
                "line was {!r}".format(firstline))
            log.critical(errmsg)
            raise ValueError(errmsg)

        for line in f.readlines():
            line = line.strip()
            if line.startswith("#"):
                log.debug("Skipping commented-out line")
                continue
                # Spike doesn't produce comments, but we can use this to
                # comment out duff lines -- FOR EXAMPLE, when the last beat
                # of the session has its DBP time being a clone of the
                # preceding beat's DBP time (presumably for lack of
                # information, but still, it doesn't make sense).
            values = [float(x) for x in line.split()]
            assert len(values) == expected_num_columns, (
                "Expecting {} columns, found {}".format(expected_num_columns,
                                                        len(values))
            )
            if col_7_always_zero:
                assert(values[7] == 0)  # null column on the end, always 0
            if (values[0] == end_time_marker_s and
                    all(x == 0 for x in values[1:])):
                log.info("End of file marker found")
                return
            # Column definitions for a Spike peak file are as follows:
            yield Heartbeat(
                cfg=cfg,
                r_time_s=values[0],
                rr_interval_ms=(values[1] if spike_rrint_in_ms
                                else values[1] * 1000),  # s to ms
                hr_bpm=values[2],
                sbp_time_s=values[3],
                sbp_mmhg=values[4],
                dbp_time_s=values[5],
                dbp_mmhg=values[6]
            )


def fetch_all_telemetry(cfg: Config,
                        filename: str) -> List[Heartbeat]:
    """
    Returns all the data from a Spike peak file as a list.
    """
    # noinspection PyTypeChecker
    telemetry = list(gen_telemetry(cfg, filename))  # type: List[Heartbeat]
    if cfg.sanity_checks:
        for i, heartbeat in enumerate(telemetry):
            if i == 0:  # no preceding beat
                continue
            preceding = telemetry[i - 1]
            # Is there a massive gap between heartbeats?
            # Note that some gap comes about through the removal of artefacts.
            r_discrepancy_s = abs(heartbeat.calc_prev_beat_r_time_s() -
                                  preceding.r_time_s)
            if r_discrepancy_s > cfg.sanity_max_rr_discrepancy_s:
                raise ValueError(
                    "Beat {i} [zero-numbered] has r_time_s={r_time_s}, "
                    "rr_interval_ms={rr_interval_ms}, "
                    "calc_prev_beat_r_time_s()={calc_prev_beat_r_time_s}, "
                    "but preceding beat {prec_i} has "
                    "r_time_s={prec_r_time_s} "
                    "(difference of {r_discrepancy_s} s exceeds "
                    "max permitted of {max_rr_discrepancy_s} s)".format(
                        i=i,
                        r_time_s=heartbeat.r_time_s,
                        rr_interval_ms=heartbeat.rr_interval_ms,
                        calc_prev_beat_r_time_s=heartbeat.calc_prev_beat_r_time_s(),  # noqa
                        prec_i=i - 1,
                        prec_r_time_s=preceding.r_time_s,
                        r_discrepancy_s=r_discrepancy_s,
                        max_rr_discrepancy_s=cfg.sanity_max_rr_discrepancy_s,
                    ))
            # Is the systolic BP for the preceding beat after this beat's R
            # wave? That'd be odd.
            if preceding.sbp_time_s > heartbeat.r_time_s:
                raise ValueError(
                    "Beat {prec_i} [zero-numbered] with "
                    "r_time_s={prec_r_time_s} has sbp_time={prec_sbp_time_s}, "
                    "but this is after the next beat's "
                    "r_time_s={r_time_s}".format(
                        prec_i=i - 1,
                        prec_r_time_s=preceding.r_time_s,
                        prec_sbp_time_s=preceding.sbp_time_s,
                        r_time_s=heartbeat.r_time_s,
                    ))
            # Is the diastolic BP for the preceding beat after this beat is
            # completely over? That'd be odd.
            if preceding.dbp_time_s > heartbeat.calc_next_beat_r_time_s():
                raise ValueError(
                    "Beat {prec_i} [zero-numbered] with "
                    "r_time_s={prec_r_time_s} has dbp_time={prec_dbp_time_s}, "
                    "but this is after the next beat's "
                    "calc_next_beat_r_time_s={calc_next_beat_r_time_s}".format(
                        prec_i=i - 1,
                        prec_r_time_s=preceding.r_time_s,
                        prec_dbp_time_s=preceding.dbp_time_s,
                        calc_next_beat_r_time_s=heartbeat.calc_next_beat_r_time_s,  # noqa
                    ))
    return telemetry


def test_spike_read(cfg: Config) -> None:
    """
    Reads all data from a Spike peak file and prints it, for testing.
    """
    filename = cfg.test_spike_filename
    log.info("Testing: reading Spike peak file {}".format(repr(filename)))
    if cfg.validate:
        telemetry = fetch_all_telemetry(cfg, filename)  # also validates
        if cfg.validate_verbose:
            for datum in telemetry:
                print(datum)
        log.info(
            "Demonstration of means for time range [{start}, {end})".format(
                start=cfg.test_start_time_s,
                end=cfg.test_end_time_s))
        info = TelemetryMeans(cfg=cfg,
                              telemetry=telemetry,
                              start_time_s=cfg.test_start_time_s,
                              end_time_s=cfg.test_end_time_s,
                              show_poincare_plot=True,
                              show_filter_response=True,
                              show_filtered_rsa=True)
        print(info)
    else:
        # noinspection PyTypeChecker
        for datum in gen_telemetry(cfg, filename):
            print(datum)
