#!/usr/bin/env python
# whisker_autonomic_analysis/trial_telemetry_record.py

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

from cardinal_pythonlib.reprfunc import simple_repr
from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Boolean, DateTime, Float, Integer, String

from .sqlalchemy_base import Base

# =============================================================================
# Constants
# =============================================================================

# Database field lengths
SUBJECT_NAME_LEN = 45  # as per the task
FILENAME_LEN = 255
AUTONOMIC_PARAM_LEN = 50
PHASE_LEN = 50


# =============================================================================
# TrialTelemetryRecord
# =============================================================================

class TrialTelemetryRecord(Base):
    """
    Database object, to store results.
    """
    __tablename__ = "TrialTelemetry"

    id = Column(Integer, primary_key=True)

    # FKs (non-enforced) from other tables.
    # I'm not sure that creating multiple different indexes is the best way
    # to go here... create a composite index instead (see below).
    date_time = Column(DateTime)
    subject = Column(String(length=SUBJECT_NAME_LEN))
    box = Column(Integer)
    trial = Column(Integer)

    peak_filename = Column(String(length=FILENAME_LEN))

    phase = Column(String(length=PHASE_LEN), index=True)
    start_time_s = Column(Float, nullable=True, index=True)
    end_time_s = Column(Float, nullable=True, index=True)

    autonomic_parameter = Column(String(length=AUTONOMIC_PARAM_LEN),
                                 index=True)
    parameter_value = Column(Float)
    is_difference = Column(Boolean)  # was this value created by subtraction, not measurement?  # noqa

    __table_args__ = (
        Index('idx_dt_subj_box_trial', 'date_time', 'subject', 'box', 'trial'),
    )

    def __repr__(self) -> str:
        return simple_repr(self, [
            "id", "date_time", "subject", "box", "trial",
            "peak_filename",
            "phase", "start_time", "end_time",
            "autonomic_parameter", "parameter_value", "is_difference"
        ])
