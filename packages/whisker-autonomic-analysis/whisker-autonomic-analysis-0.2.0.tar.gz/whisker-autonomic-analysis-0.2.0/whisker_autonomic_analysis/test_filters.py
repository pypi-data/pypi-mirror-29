#!/usr/bin/env python
# whisker_autonomic_analysis/test_filters.py

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
import pprint
from typing import List, Tuple

import numpy as np

from .config import Config
from .maths import coordinates_from_x_y
from .timeseries import filter_time_series

log = logging.getLogger(__name__)


def test_filters(cfg: Config,
                 freq_amp_pairs: List[Tuple[float, float]],
                 sampling_freq_hz: float = None,
                 duration_s: float = 400,
                 numtaps: int = None,
                 low_cutoff_hz: float = None,
                 high_cutoff_hz: float = None,
                 show_filter_response: bool = False,
                 log_freq_in_spectrum: bool = True,
                 test_strip_last_number: bool = False,
                 debug: bool = False) -> None:
    log.info("Testing filters")

    # Filter parameters
    numtaps = numtaps or cfg.rsa_numtaps
    low_cutoff_hz = low_cutoff_hz or cfg.rsa_low_cutoff_hz
    high_cutoff_hz = high_cutoff_hz or cfg.rsa_high_cutoff_hz

    # Signal parameters
    sampling_freq_hz = sampling_freq_hz or cfg.hrv_resample_freq_hz

    # Make signal
    n = int(duration_s * sampling_freq_hz)
    assert n > 0, "No samples, with duration_s={}, sampling_freq_hz={}".format(
        duration_s, sampling_freq_hz)
    y = np.zeros(n)
    t = np.linspace(0.0, duration_s, num=n)
    for freq, amp in freq_amp_pairs:
        y += amp * np.sin(2 * np.pi * t * freq)
    if test_strip_last_number:  # e.g. check FFT with odd/even sample size
        t = t[:-1]
        y = y[:-1]
    time_series_coords = coordinates_from_x_y(t, y)

    log.info("test_filters:\n" + pprint.pformat({
        'n': n,
        'sampling_freq_hz': sampling_freq_hz,
        'duration_s': duration_s,
        'freq_amp_pairs': freq_amp_pairs,
    }))
    if debug:
        log.debug("test_filters:\n" + pprint.pformat({
            't': t,
            'y': y,
        }))

    filter_time_series(
        time_series=time_series_coords,
        numtaps=numtaps,
        low_cutoff_hz=low_cutoff_hz,
        high_cutoff_hz=high_cutoff_hz,
        sampling_freq_hz=sampling_freq_hz,
        show_filter_response=show_filter_response,
        show_plot=True,
        log_freq_in_spectrum=log_freq_in_spectrum,
    )  # result ignored
