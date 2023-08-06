#!/usr/bin/env python
# whisker_autonomic_analysis/aversive_pavlovian_database.py

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
from typing import Generator, List

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text

from .config import Config
from .maths import to_db_float
from .session_definition import SessionDefinition
from .spike_file import fetch_all_telemetry
from .stimulus_locked_telemetry import StimulusLockedTelemetry
from .telemetry_means import TelemetryMeans
from .trial_telemetry_record import TrialTelemetryRecord
from .trial_timing import TrialTiming

log = logging.getLogger(__name__)


WHOLE_SESSION_PHASE = "whole_session"
WHOLE_SESSION_TRIAL_NUM = -1


def fetch_trial_timings(
        connection: Connection,
        session_definition: SessionDefinition) -> List[TrialTiming]:
    # http://docs.sqlalchemy.org/en/rel_0_9/core/sqlelement.html#sqlalchemy.sql.expression.text  # noqa
    result = connection.execute(
        text("""
SELECT
    Trial,
    TrialStartTimeSec,
    CSStartTimeSec,
    CSStopTimeSec,
    USStartTimeSec,
    USStopTimeSec,
    ITIEndTimeSec
FROM
    TrialRecords
WHERE
    DateTimeCode = :date_time_code
    AND Subject = :subject
    AND Box = :box
ORDER BY
    Trial
        """),
        date_time_code=session_definition.date_time,
        subject=session_definition.subject,
        box=session_definition.box,
    )
    trial_timings = []  # type: List[TrialTiming]
    for row in result:
        trial_start = row['TrialStartTimeSec']  # Laith doesn't care  # but Hannah does  # noqa
        cs_start = row['CSStartTimeSec']
        cs_stop = row['CSStopTimeSec']
        us_start = row['USStartTimeSec']
        us_stop = row['USStopTimeSec']
        iti_end = row['ITIEndTimeSec']
        # Before Laith's changes:
        #   baseline_start = trial_start
        # Next "if" bit by Laith 2017-05-03, for v0.1.9, rephrased by RNC:
        if cs_stop < us_start:  # CS, gap, US
            cs_length = cs_stop - cs_start
            baseline_start = cs_start - cs_length
            # ... baseline is a period of equal length to the CS, before the
            # CS starts (but we won't allow baseline to begin before the trial
            # does)
            # ... allowed to start before trial_start, subsequently!
        else:  # CS coterminates in US, or CS continues through US
            cs_alone_length = us_start - cs_start
            baseline_start = cs_start - cs_alone_length
            # ... baseline is a period of equal length to the "CS alone" period
            # before the CS starts (but we won't allow time before the trial).
            # ... allowed to start before trial_start
        tt = TrialTiming(session_definition=session_definition,
                         trial_number=row['Trial'],
                         trial_start=trial_start,
                         baseline_start_time_s=baseline_start,
                         cs_on_time_s=cs_start,
                         cs_off_time_s=cs_stop,
                         us_on_time_s=us_start,
                         us_off_time_s=us_stop,
                         iti_end=iti_end)
        trial_timings.append(tt)
    return trial_timings


def delete_existing_results(dbsession: Session,
                            session_definition: SessionDefinition) -> None:
    log.debug("Deleting existing results for session: {}".format(
        session_definition))
    dbsession.query(TrialTelemetryRecord).filter(
        TrialTelemetryRecord.date_time == session_definition.date_time,
        TrialTelemetryRecord.subject == session_definition.subject,
        TrialTelemetryRecord.box == session_definition.box
    ).delete()
    # See also http://stackoverflow.com/questions/39773560/sqlalchemy-how-do-you-delete-multiple-rows-without-querying  # noqa
    log.debug("... commit")
    dbsession.commit()
    log.debug("... done")


def process_session(cfg: Config,
                    session_definition: SessionDefinition,
                    kb_timings: List[TrialTiming] = None,
                    session_start_s: float = None,
                    session_end_s: float = None) -> None:
    kb_timings = kb_timings or []  # type: List[TrialTiming]
    log.info("Processing session: {}".format(session_definition))
    # Fetch data
    if kb_timings:
        trial_timings = kb_timings
    else:
        trial_timings = fetch_trial_timings(
            connection=cfg.connection,
            session_definition=session_definition)
    if not trial_timings:
        log.warning("No trial timings for session definition "
                    "{}".format(session_definition))
        return
    spike_peak_filename = session_definition.get_peak_filename()
    telemetry = fetch_all_telemetry(cfg, spike_peak_filename)

    # Do some thinking, and save results to the output database
    if not cfg.skip_if_results_exist:
        delete_existing_results(dbsession=cfg.session,
                                session_definition=session_definition)
    for trial_timing in trial_timings:
        log.info("... processing trial: {}".format(trial_timing))
        slt = StimulusLockedTelemetry(telemetry=telemetry,
                                      trial_timing=trial_timing,
                                      cfg=cfg,
                                      peak_filename=spike_peak_filename)
        # noinspection PyTypeChecker
        for ttr in slt.gen_trial_telemetry_records():
            cfg.session.add(ttr)

    # Added 2018-03-08: whole-session analysis
    log.info("... processing entire session")
    if session_start_s is None:
        session_start_s = trial_timings[0].trial_start  # start of first trial
    if session_end_s is None:
        session_end_s = trial_timings[-1].iti_end  # end (after ITI) of last trial  # noqa
    sd = session_definition
    tm = TelemetryMeans(cfg=cfg,
                        telemetry=telemetry,
                        start_time_s=session_start_s,
                        end_time_s=session_end_s)
    for ap, value in tm.get_parameters().items():
        ttr = TrialTelemetryRecord(
            date_time=sd.date_time,
            subject=sd.subject,
            box=sd.box,
            trial=WHOLE_SESSION_TRIAL_NUM,
            peak_filename=spike_peak_filename,
            phase=WHOLE_SESSION_PHASE,
            start_time_s=session_start_s,
            end_time_s=session_end_s,
            autonomic_parameter=ap,
            parameter_value=to_db_float(value),
            is_difference=False,
        )
        cfg.session.add(ttr)

    log.debug("... commit")
    cfg.session.commit()

    # 2018-03-08: write RR interval file?
    if cfg.write_rr_interval_files:
        filename = "rr_intervals_{s}_{dt}.txt".format(
            s=session_definition.subject,
            dt=session_definition.date_time.strftime("%Y-%m-%d_%H%M"),  # e.g. 2001-12-31_1031  # noqa
        )
        with open(filename, 'w') as f:
            for heartbeat in telemetry:
                # Kubios wants one number per row. It may autodetect s vs ms.
                # Certainly seconds works.
                f.write("{}\n".format(heartbeat.rr_interval_s))

    log.debug("... done")


def gen_session_definitions(cfg: Config) -> Generator[SessionDefinition, None,
                                                      None]:
    sql = """
SELECT
    DateTimeCode,
    Subject,
    Box,
    ChunkDurationSec
FROM
    SessionsForAutonomicAnalysis AS s
    """
    # - Prior to v0.1.5 (2017-04-11), we were selecting from the Config table.
    #   We just replace that with SessionsForAutonomicAnalysis, to have a
    #   manually curated table instead. (It's still aliased to 'c' so we don't
    #   need to change the add-on bit below.)
    # - Added ChunkDurationSec, v0.1.7
    if cfg.skip_if_results_exist:
        sql += """
WHERE NOT EXISTS (
    SELECT * FROM {telemetry_table} AS tt
    WHERE
        tt.date_time = s.DateTimeCode  -- both DATETIME
        AND tt.subject = s.Subject  -- both VARCHAR
        AND tt.box = s.Box  -- both INT
)
        """.format(
            telemetry_table=TrialTelemetryRecord.__tablename__,
        )
    result = cfg.connection.execute(text(sql))
    for row in result:
        yield SessionDefinition(date_time=row[0],
                                subject=row[1],
                                box=row[2],
                                chunk_duration_s=row[3],
                                peakfile_base_dir=cfg.peak_dir)
