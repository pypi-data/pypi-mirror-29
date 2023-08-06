#!/usr/bin/env python
# whisker_autonomic_analysis/config.py

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

from enum import Enum
import logging
import tempfile
from typing import Optional

from cardinal_pythonlib.reprfunc import auto_str, auto_repr
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================

class SourceMethod(Enum):
    AVPAVDB = "AversivePavlovian database from 2012- code by Rudolf Cardinal"
    AVPAVOLDTXT = "AversivePavlovian text files from old code by Katrin Braesicke"  # noqa


# =============================================================================
# Config object, to save passing around lots of configuration parameters (we
# can just pass around one).
# =============================================================================

class Config(object):
    def __init__(self,
                 source: SourceMethod,
                 connection: Optional[Connection],
                 engine: Optional[Engine],
                 hrvtk_cd_to_get_hrv: bool,
                 hrv: bool,
                 hrv_builtin: bool,
                 hrvtk_get_hrv_filename: str,
                 hrv_resample_freq_hz: float,
                 peak_dir: str,
                 rsa_low_cutoff_hz: float,
                 rsa_high_cutoff_hz: float,
                 rsa_numtaps: int,
                 sanity_checks: bool,
                 sanity_max_rr_discrepancy_s: float,
                 session: Optional[Session],
                 skip_if_results_exist: bool,
                 test_end_time_s: Optional[float],
                 test_spike_filename: str,
                 test_start_time_s: Optional[float],
                 validate: bool,
                 valid_bp_min_mmhg: float,
                 valid_bp_max_mmhg: float,
                 valid_hr_min_bpm: float,
                 valid_hr_max_bpm: float,
                 valid_max_hr_error_bpm: float,
                 validate_verbose: bool,
                 write_rr_interval_files: bool) -> None:
        self.source = source
        self.connection = connection
        self.engine = engine
        self.hrv = hrv
        self.hrv_builtin = hrv_builtin
        self.hrvtk_cd_to_get_hrv = hrvtk_cd_to_get_hrv
        self.hrvtk_get_hrv_filename = hrvtk_get_hrv_filename
        self.hrv_resample_freq_hz = hrv_resample_freq_hz
        self.peak_dir = peak_dir
        self.rsa_high_cutoff_hz = rsa_high_cutoff_hz
        self.rsa_low_cutoff_hz = rsa_low_cutoff_hz
        self.rsa_numtaps = rsa_numtaps
        self.sanity_checks = sanity_checks
        self.sanity_max_rr_discrepancy_s = sanity_max_rr_discrepancy_s
        self.session = session
        self.skip_if_results_exist = skip_if_results_exist
        self.test_end_time_s = test_end_time_s
        self.test_spike_filename = test_spike_filename
        self.test_start_time_s = test_start_time_s
        self.validate = validate
        self.valid_bp_min_mmhg = valid_bp_min_mmhg
        self.valid_bp_max_mmhg = valid_bp_max_mmhg
        self.valid_hr_min_bpm = valid_hr_min_bpm
        self.valid_hr_max_bpm = valid_hr_max_bpm
        self.valid_max_hr_error_bpm = valid_max_hr_error_bpm
        self.validate_verbose = validate_verbose
        self.write_rr_interval_files = write_rr_interval_files

        self.tempdir = tempfile.TemporaryDirectory()
        log.debug("Creating temporary directory " + repr(self.tempdir.name))
        # ... autodeleted when the object goes out of scope; see
        #     https://docs.python.org/3/library/tempfile.html
        # ... which manages it using weakref.finalize
        # ... the Config object is a nice one to have manage this scope

    def __repr__(self) -> str:
        return auto_repr(self)

    def __str__(self) -> str:
        return auto_str(self)
