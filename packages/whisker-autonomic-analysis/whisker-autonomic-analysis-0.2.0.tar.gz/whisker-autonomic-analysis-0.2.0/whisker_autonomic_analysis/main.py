#!/usr/bin/env python
# whisker_autonomic_analysis/main.py

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

- Program to analyse, jointly,
  (1) "Peak" files, created like this:
        - telemetry device measuring blood pressure
        -> Spike software
        -> filter (written by Katrin Braesicke, in Spike) to remove
           non-physiological outliers
        -> text file

  (2) Stimulus timing information, either as textfile or relational database
      output from a specific Whisker task, AversivePavlovian (originally
      written by KB, then recoded by Rudolf Cardinal).

- First version: 2017-03-10.

- Note that we have no absolutely reliable way to predict "peak" file names.
  So we offer the user a manual choice, via a GUI.

- REFERENCES

[1]  https://en.wikipedia.org/wiki/Heart_rate_variability
[2]  Allen 2002
     http://apsychoserver.psych.arizona.edu/JJBAReprints/SPR2002/Allen_SPR2002.pdf
[3]  Allen
     http://apsychoserver.psych.arizona.edu/JJBAReprints/CMet/How%20to%20Reduce%20ekg%20data.htm
[4]  Toichi et al. 1997
     https://www.ncbi.nlm.nih.gov/pubmed/9021653
[5]  Lorenz 1963 "Deterministic nonperiodic flow"
     http://dx.doi.org/10.1175/1520-0469(1963)020%3C0130:DNF%3E2.0.CO;2
[6]  https://en.wikipedia.org/wiki/Poincar%C3%A9_plot
[7]  Grossman P
     https://www.researchgate.net/post/Is_there_a_standardized_method_for_measuring_vagal_tone
[8]  https://en.wikipedia.org/wiki/Unevenly_spaced_time_series
[9]  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1564191/
[10] HRV Toolkit
     https://physionet.org/tutorials/hrv-toolkit/

- TO DO:

*** Check scaling of output variables.
    For example: ln_rsa: was it expecting its IBIs in s, or ms? Etc.

*** Finish adding support for HRV Toolkit (requires extra tools that it looks for)

"""  # noqa

# Python standard library
import argparse
from enum import Enum
import logging
import os
import tkinter.filedialog
from typing import Dict, List, Tuple, Type

# Third-party imports
from cardinal_pythonlib.datetimefunc import coerce_to_datetime
from cardinal_pythonlib.debugging import pdb_run
from cardinal_pythonlib.logs import main_only_quicksetup_rootlogger
from pendulum import Pendulum
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# Imports from this package
from .aversive_pavlovian_database import (gen_session_definitions,
                                          process_session)
from .config import Config, SourceMethod
from .gui import tkinter_guard_invisible_root
from .session_definition import SessionDefinition
from .sqlalchemy_base import Base
from .test_filters import test_filters
from .trial_timing import TrialTiming
from .spike_file import test_spike_read
from .version import VERSION, VERSION_DATE

log = logging.getLogger(__name__)


# =============================================================================
# Constants
# =============================================================================

LOG_EQUISPACED_TEST_FREQS = [
    (0.01, 1),
    # (0.0316, 1),
    (0.1, 1),
    # (0.316, 1),
    # (1, 1),
    # (3.16, 1),
]
LINEAR_EQUISPACED_TEST_FREQS = [
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
]


# =============================================================================
# Helper functions
# =============================================================================

def keys_descriptions_default_from_enum(
        enum: Type[Enum],
        sort_keys: bool = False,
        key_to_description: str = ": ",
        joiner: str = " // ") -> Tuple[List[str], str, str]:
    keys = [e.name for e in enum]
    default = keys[0]
    if sort_keys:
        keys.sort()
    descriptions = [
        "{k}{k2d}{d}".format(
            k=k,
            k2d=key_to_description,
            d=enum[k].value,
        )
        for k in keys
    ]
    description_str = joiner.join(descriptions)
    return keys, description_str, default


def get_old_kb_text_filename(peakdir: str) -> str:
    with tkinter_guard_invisible_root() as _:
        opentitle = "Open Braesicke AversivePavlovian results (onset times) file"  # noqa
        return tkinter.filedialog.askopenfilename(
            initialdir=peakdir,
            title=opentitle,
            filetypes=(('All files', '*'),
                       ('Text files', '*.txt'))
        )


# =============================================================================
# Main ways of handling input
# =============================================================================

def process_aversive_pavlovian_db_source(cfg: Config) -> None:
    # Process all sessions found in database
    # noinspection PyTypeChecker
    log.info("Processing available sessions.")
    if cfg.skip_if_results_exist:
        log.info("... skipping any sessions for which telemetry data exists")
    count = 0
    # noinspection PyTypeChecker
    for session_definition in gen_session_definitions(cfg):
        process_session(cfg=cfg, session_definition=session_definition)
        count += 1
    log.info("All sessions processed: count = {}.".format(count))


def process_aversive_pavlovian_kb_txt_source(cfg: Config) -> None:
    """
    Use text output from the old AversivePavlovian task by Katrin Braesicke.
    This preceded Rudolf Cardinal's 2012- rewrite (which moved to databases and
        more structured text files), but the KB version remained in use
        subsequently.

CONTENT

This is a standard session with only the houselight on.
  Monkey is Parnsip
The session has a waiting time at the beginning of 0s.
     Each CS1 has a length of 20s.     The source for the CS1  is ticktock.wav
     There is no US
     Each CS2 has a length of 0s.     The source for the CS2 is the sound generator
     There is no US
DateTimeCode:21/05/2015 10:55:13
  60       80       80   'CS1'    '1'
  150       170       170   'CS2'    '1'
  210       210       210   'CS3'    '2'
  290       290       290   'CS4'    '2'
  350       370       370   'CS5'    '1'
  420       440       440   'CS6'    '1'
  480       500       500   'CS7'    '1'
  550       550       550   'CS8'    '2'
  600       600       600   'CS9'    '2'
  660       680       680   'CS10'    '1'
  750       770       770   'CS11'    '1'
  850       850       850   'CS12'    '2'
  890       910       910   'CS13'    '1'
  970       970       970   'CS14'    '2'
  1050       1050       1050   'CS15'    '2'
  1130       1130       1130   'CS16'    '2'
  1200       1220       1220   'CS17'    '1'
  1270       1290       1290   'CS18'    '1'
  1350       1370       1370   'CS19'    '1'
  1430       1430       1430   'CS20'    '2'
  1500       1500       1500   'CS21'    '2'
  1580       1580       1580   'CS22'    '2'
  1620       1640       1640   'CS23'    '1'
  1710       1710       1710   'CS24'    '2'
session ends	1800
DateTimeCode,Filename,Subject
21/05/2015 11:25:14,Parsnip_Cueprobe2-mGluR_21May15.txt,Parnsip

EXPLANATION
    column 0 -- CS onset
    column 1 -- CS offset
    column 2 -- US onset
    column 3 -- CS sequence number as text
    column 4 -- '1' or '2' meaning CS/US type number (as in "Each CS1 has...")

    """  # noqa
    datetime_prefix = "DateTimeCode:"
    monkey_prefix = "Monkey is "
    session_ends_prefix = "session ends"
    cs_prefix = "CS"
    each_cs_prefix = "Each CS"
    no_cs_line = "There is no US"

    unknown_box = -1
    default_chunk_duration_s = 10000  # stupid large number resulting in 1 chunk per thing  # noqa ***
    assert not cfg.skip_if_results_exist, (
        "For this input method, DO NOT set skip_if_results_exist (too much "
        "potential to confuse a manual operator by doing nothing)."
    )
    results_filename = get_old_kb_text_filename(peakdir=cfg.peak_dir)
    if not results_filename:
        log.info("No file chosen; exiting")
        return
    session_definition = None  # type: SessionDefinition
    datetimecode = None
    kb_timings = []  # type: List[TrialTiming]
    session_start_s = 0  # always
    session_end_s = None  # type: float
    in_main = False
    us_durations = {}  # type: Dict[int, float]
    current_cs = -1  # a silly number
    with open(results_filename) as f:
        for line in f.readlines():
            line = line.strip()  # e.g. remove leading/trailing space/newline
            if line.startswith(monkey_prefix):
                subject = line[len(monkey_prefix):]
                log.debug("Found subject: {}".format(subject))
            elif line.startswith(each_cs_prefix):
                current_cs = int(line[len(each_cs_prefix):].split()[0])
                log.debug("Found CS type: {}".format(current_cs))
            elif line == no_cs_line:
                log.debug("US is absent for CS type {}".format(current_cs))
                us_durations[current_cs] = 0
            # NOTE: non-zero US durations NOT CURRENTLY SUPPORTED.
            elif line.startswith(datetime_prefix):
                datetimecode = Pendulum.parse(line[len(datetime_prefix):])
                datetimecode = coerce_to_datetime(datetimecode)
                log.debug("Found datetimecode: {}".format(datetimecode))
                session_definition = SessionDefinition(
                    date_time=datetimecode,
                    subject=subject,
                    box=unknown_box,
                    chunk_duration_s=default_chunk_duration_s,
                    peakfile_base_dir=cfg.peak_dir
                )
                in_main = True
            elif line.startswith(session_ends_prefix):
                in_main = False
                session_end_s = float(line[len(session_ends_prefix):])
                log.debug("Session ends at {}".format(session_end_s))
            elif in_main:
                assert session_definition is not None, (
                    "Haven't seen subject yet!")
                parts = line.split()
                cs_onset_s = float(parts[0])
                cs_offset_s = float(parts[1])
                us_onset_s = float(parts[2])
                trial_number = int(parts[3].strip("'")[len(cs_prefix):])
                cs_us_type = int(parts[4].strip("'"))
                # As before, baseline is a period of equal length to the CS,
                # before the CS starts (is allowed to precede trial start, too)
                cs_duration_s = cs_offset_s - cs_onset_s
                baseline_start_s = cs_onset_s - cs_duration_s
                us_duration_s = us_durations[cs_us_type]
                us_offset_s = us_onset_s + us_duration_s
                tt = TrialTiming(
                    session_definition=session_definition,
                    trial_number=trial_number,
                    trial_start=cs_onset_s,  # in Katrin world
                    baseline_start_time_s=baseline_start_s,
                    cs_on_time_s=cs_onset_s,
                    cs_off_time_s=cs_offset_s,
                    us_on_time_s=us_onset_s,
                    us_off_time_s=us_offset_s,
                    iti_end=None,  # unused for this
                )
                log.debug("Found trial timings: {}".format(tt))
                kb_timings.append(tt)
    assert datetimecode is not None, "Can't find date/time code"
    assert session_end_s is not None, "Can't find session end time"
    assert kb_timings, "Didn't find any trials"
    process_session(
        cfg=cfg,
        session_definition=session_definition,
        kb_timings=kb_timings,
        session_start_s=session_start_s,
        session_end_s=session_end_s,
    )


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    main_only_quicksetup_rootlogger()
    thisdir = os.path.abspath(os.path.dirname(__file__))

    # Command-line arguments
    progtitle = (
        "whisker_autonomic_analysis, "
        "version {version} ({version_date}), by Rudolf Cardinal.".format(
            version=VERSION, version_date=VERSION_DATE))
    progdesc = progtitle + (
        " Takes data from (1) the database created by the AversivePavlovian "
        "Whisker behavioural task, and (2) Spike output of blood pressure "
        "telemetry data. Then (3) creates stimulus-related measures of "
        "autonomic activity, and (4) stashes them back in the database."
    )
    parser = argparse.ArgumentParser(
        description=progdesc,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # General settings

    parser.add_argument(
        '--version', action='store_true',
        help="Print version (and stop).",
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help="Be verbose.",
    )
    m_k, m_desc, m_default = keys_descriptions_default_from_enum(
        SourceMethod)
    parser.add_argument(
        "--source", type=str, choices=m_k,
        default=m_default,
        help="Where should we find our source data? ({})".format(m_desc)
    )
    parser.add_argument(
        "--write_rr_interval_files", action="store_true",
        help="Write RR interval files to current directory."
    )

    # Database settings

    dbgroup = parser.add_argument_group('Database', 'Database settings')
    dbgroup.add_argument(
        '--dburl',
        help="Specify the SQLAlchemy URL to find the database for output "
             "(and, for the AVPAV method, this is also the AversivePavlovian "
             "database for input)",
    )
    dbgroup.add_argument(
        '--skip_if_results_exist', action='store_true',
        help="Skip any sessions (in the database) for which any telemetry "
             "results already exist"
    )
    dbgroup.add_argument(
        '--no_skip_if_results_exist', action='store_false',
        dest='skip_if_results_exist',
        help="Opposite of --skip_if_results_exist: if telemetry results "
             "exist, delete existing results and redo",
    )
    dbgroup.set_defaults(skip_if_results_exist=True)

    # Spike data settings

    spikegroup = parser.add_argument_group(
        'Spike', 'Settings for loading Spike autonomic data files')
    spikegroup.add_argument(
        '--peakdir', default=thisdir,
        help="Specify the directory where Spike peak files live "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--sanity_checks', action='store_true',
        help="Check for e.g. big gaps in telemetry during Spike file loading",
    )
    spikegroup.add_argument(
        '--no_sanity_checks', dest='sanity_checks', action='store_false',
        help="Opposite of --sanity_checks",
    )
    spikegroup.set_defaults(sanity_checks=True)
    spikegroup.add_argument(
        '--sanity_max_rr_discrepancy_s', type=float, default=10,
        help="For sanity checks: maximum permitted R-R discrepancy between "
             "times of consecutive beats and stated IBI (s) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--validate', action='store_true',
        help="Validate during Spike file loading",
    )
    spikegroup.add_argument(
        '--no_validate', dest='validate', action='store_false',
        help="Opposite of --validate",
    )
    spikegroup.set_defaults(validate=True)
    spikegroup.add_argument(
        '--validate_verbose', action='store_true',
        help="Report all data read during Spike file loading",
    )
    spikegroup.add_argument(
        '--valid_bp_min_mmhg', type=float, default=10,
        help="For validation: minimum blood pressure (mmHg) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--valid_bp_max_mmhg', type=float, default=300,
        help="For validation: maximum blood pressure (mmHg) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--valid_hr_min_bpm', type=float, default=10,
        help="For validation: minimum heart rate (beats per minute) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--valid_hr_max_bpm', type=float, default=600,  # it does go over 410!
        help="For validation: maximum heart rate (beats per minute) "
             "(default: %(default)s)",
    )
    spikegroup.add_argument(
        '--valid_max_hr_error_bpm', type=float, default=1,
        help="For validation: maximum permissible discrepancy between heart "
             "rate stated and heart rate calculated from interbeat interval "
             "(bpm)",
    )

    # HRV calculations

    hrvgroup = parser.add_argument_group(
        'HRV', 'Settings for built-in heart-rate variability calculations')
    hrvgroup.add_argument(
        '--hrv', action='store_true',
        help="Add heart-rate variability (HRV) measures, either using built-in"
             " calculations or external tools",
    )
    hrvgroup.add_argument(
        '--no_hrv', dest='hrv', action='store_false',
        help="Opposite of --hrv",
    )
    hrvgroup.set_defaults(hrv=True)
    hrvgroup.add_argument(
        '--hrv_builtin', action='store_true',
        help="Add built-in HRV measures",
    )
    hrvgroup.add_argument(
        '--no_hrv_builtin', dest='hrv_builtin', action='store_false',
        help="Opposite of --hrv_builtin",
    )
    hrvgroup.set_defaults(hrv_builtin=True)
    hrvgroup.add_argument(
        '--hrv_resample_freq_hz', type=float, default=10,
        help="Resampling frequency to create time series from interbeat "
             "intervals (IBIs), for some heart rate variability (HRV) "
             "calculations",
    )
    hrvgroup.add_argument(
        '--rsa_low_cutoff_hz', type=float, default=0.12,
        help="Low frequency cutoff for bandpass filter (amplitude is 0.5 "
             "at this frequency) for respiratory sinus arrhythmia (RSA) "
             "calculations",
    )
    hrvgroup.add_argument(
        '--rsa_high_cutoff_hz', type=float, default=0.4,
        help="High frequency cutoff for bandpass filter (amplitude is 0.5 "
             "at this frequency) for respiratory sinus arrhythmia (RSA) "
             "calculations",
    )
    hrvgroup.add_argument(
        '--rsa_numtaps', type=int, default=241,
        help="Number of taps for the fixed-impulse-response (FIR) filter used "
             "for RSA analysis",
    )

    # External tool settings

    toolgroup = parser.add_argument_group('Tools', 'External tool settings')
    toolgroup.add_argument(
        '--get_hrv_filename',
        help="Specify the path to the get_hrv tool (from the HRV Toolkit, "
             "https://physionet.org/tutorials/hrv-toolkit/)",
    )
    toolgroup.add_argument(
        '--cd_to_get_hrv', action='store_true',
        help="Change to the directory of the get_hrv tool to run it?",
    )
    toolgroup.add_argument(
        '--no_cd_to_get_hrv', dest='cd_to_get_hrv', action='store_false',
        help="Opposite of --cd_to_get_hrv",
    )
    toolgroup.set_defaults(cd_to_get_hrv=True)  # doesn't help under Linux; use the PATH instead  # noqa

    # Testing

    testgroup = parser.add_argument_group('Test', 'Options for testing')
    testgroup.add_argument(
        '--test_filters', action='store_true',
        help="Test filter system (then stop)",
    )
    testgroup.add_argument(
        '--test_spike',
        help="Specify a Spike output filename to test with (then stop)",
    )
    testgroup.add_argument(
        '--test_start_time_s', type=float,
        help="Start time (s) [INCLUSIVE] to analyse test Spike data (if you "
             "don't specify test_start_time_s / test_end_time_s, the whole "
             "file will be used)",
    )
    testgroup.add_argument(
        '--test_end_time_s', type=float,
        help="End time (s) [EXCLUSIVE] to analyse test Spike data (if you "
             "don't specify test_start_time_s / test_end_time_s, the whole "
             "file will be used)",
    )

    progargs = parser.parse_args()
    if progargs.version:
        print("VERSION: {}\nVERSION_DATE: {}".format(VERSION, VERSION_DATE))
        return
    log.setLevel(logging.DEBUG if progargs.verbose else logging.INFO)
    log.info(progtitle)
    log.debug("Arguments: {}".format(progargs))

    def abspath_if_given(x):
        return os.path.abspath(x) if x else ''

    db_required = not (progargs.test_filters or progargs.test_spike)

    # Create config object
    if db_required:
        # Database connection required
        if not progargs.dburl:
            raise ValueError("Database URL not specified. Try --help.")
        engine = create_engine(progargs.dburl)
        log.info("Connected to database: {}".format(engine))  # hides password
        log.info("Creating any output tables that don't exist...")
        Base.metadata.create_all(engine)
        connection = engine.connect()
        session = sessionmaker(bind=engine)()
    else:
        # No database connection required
        engine = None
        connection = None
        session = None
    cfg = Config(
        source=SourceMethod[progargs.source],
        connection=connection,
        engine=engine,
        hrvtk_cd_to_get_hrv=progargs.cd_to_get_hrv,
        hrvtk_get_hrv_filename=abspath_if_given(progargs.get_hrv_filename),
        hrv=progargs.hrv,
        hrv_builtin=progargs.hrv_builtin,
        hrv_resample_freq_hz=progargs.hrv_resample_freq_hz,
        peak_dir=progargs.peakdir,
        rsa_high_cutoff_hz=progargs.rsa_high_cutoff_hz,
        rsa_low_cutoff_hz=progargs.rsa_low_cutoff_hz,
        rsa_numtaps=progargs.rsa_numtaps,
        sanity_checks=progargs.sanity_checks,
        sanity_max_rr_discrepancy_s=progargs.sanity_max_rr_discrepancy_s,
        session=session,
        skip_if_results_exist=progargs.skip_if_results_exist,
        test_end_time_s=progargs.test_end_time_s,
        test_spike_filename=abspath_if_given(progargs.test_spike),
        test_start_time_s=progargs.test_start_time_s,
        validate=progargs.validate,
        valid_bp_min_mmhg=progargs.valid_bp_min_mmhg,
        valid_bp_max_mmhg=progargs.valid_bp_max_mmhg,
        valid_hr_min_bpm=progargs.valid_hr_min_bpm,
        valid_hr_max_bpm=progargs.valid_hr_max_bpm,
        valid_max_hr_error_bpm=progargs.valid_max_hr_error_bpm,
        validate_verbose=progargs.validate_verbose,
        write_rr_interval_files=progargs.write_rr_interval_files,
    )
    log.info("Configuration:\n{}".format(cfg))

    # Do a test run and quit?
    if progargs.test_filters:
        test_filters(cfg, freq_amp_pairs=LOG_EQUISPACED_TEST_FREQS,
                     show_filter_response=True)
        test_filters(cfg, freq_amp_pairs=LINEAR_EQUISPACED_TEST_FREQS)
        return
    if progargs.test_spike:
        test_spike_read(cfg)
        return

    if cfg.source == SourceMethod.AVPAVDB:
        process_aversive_pavlovian_db_source(cfg=cfg)
    elif cfg.source == SourceMethod.AVPAVOLDTXT:
        process_aversive_pavlovian_kb_txt_source(cfg=cfg)
    else:
        assert "Bad source method (bug)"


# =============================================================================
# Command-line entry point
# =============================================================================

if __name__ == '__main__':
    with_pdb = False  # for debugging only
    if with_pdb:
        pdb_run(main)
    else:
        main()
