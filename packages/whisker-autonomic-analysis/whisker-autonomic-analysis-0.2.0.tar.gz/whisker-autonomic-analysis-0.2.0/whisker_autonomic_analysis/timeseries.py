#!/usr/bin/env python
# whisker_autonomic_analysis/timeseries.py

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
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack, signal

from .maths import coordinates_from_x_y, s_from_ms, x_y_from_coordinates

log = logging.getLogger(__name__)


# =============================================================================
# Time series and signal processing
# =============================================================================

def time_series_from_ibi(ibi_ms: np.ndarray,
                         frequency_hz: float) -> np.ndarray:
    # Operate in seconds:
    ibi_s = s_from_ms(ibi_ms)
    existing_y = ibi_s
    existing_x = np.cumsum(ibi_s)

    # NO: unequally spaced time series:
    #
    # target_x = np.unique(np.concatenate((
    #     existing_x,
    #     np.arange(0, np.max(existing_x), step=(1 / frequency_hz))
    # )))  # output from unique is guaranteed to be sorted

    # YES [8]: equal spacing:
    target_x = np.arange(0, np.max(existing_x), step=(1 / frequency_hz))

    return coordinates_from_x_y(
        x=target_x,
        y=np.interp(x=target_x, xp=existing_x, fp=existing_y)
    )


def make_filter(numtaps: int,
                sampling_freq_hz: float,
                low_cutoff_hz: float,
                high_cutoff_hz: float,
                show_plot: bool = False) -> np.ndarray:
    # - e.g. 241-point FIR filter with 0.12-0.40 Hz bandpass, and Hamming
    #   window, as per [2]
    # - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html  # noqa
    # - http://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units  # noqa
    nyquist_hz = 0.5 * sampling_freq_hz
    cutoff_hz = np.array([low_cutoff_hz, high_cutoff_hz])
    # normalized_cutoff = cutoff_hz / nyq
    filter_taps = signal.firwin(numtaps=numtaps,
                                cutoff=cutoff_hz,
                                window='hamming',
                                pass_zero=False,
                                nyq=nyquist_hz)
    # ... I think you can pass cutoff=normalized_cutoff and leave nyq=1.0,
    # or pass cutoff=cutoff_hz and nyq=nyq.

    # [9] says the cutoffs are half-amplitude frequencies, confirmed by
    # [2, fig. 2]. Yes, that's what we're getting.
    if show_plot:
        plot_filter_response(filter_taps=filter_taps,
                             sampling_freq_hz=sampling_freq_hz,
                             low_cutoff_hz=low_cutoff_hz,
                             high_cutoff_hz=high_cutoff_hz)
    return filter_taps


def fft_x_y(time_series: np.ndarray,
            sampling_freq_hz: float,
            debug: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    """
    :param time_series: series to FFT
    :param sampling_freq_hz: sampling frequency (Hz)
    :param debug: boolean
        Print verbose detail?
    :return: tuple: (x values in Hz, y values as power in decibels)
    """
    # 0. scipy.fftpack.fft gives a result of same length as the input, whether
    #    input length is even or odd.
    # 1. The conventional packing of the result, as per scipy.fftpack.fft:
    #    if A = fft(a, n), is:
    #       - A[0] is the zero-frequency term
    #       - A[1:n/2] = contains the positive-frequency terms (n/2 - 1 items)
    #       - A[n/2:] contains the negative-frequency terms (n/2 items)
    #       - if n is even, A[n/2] contains the sum of positive- and negative-
    #         frequency terms
    #    Simple example: n=8:
    #       a[0] = zero-frequency
    #       a[1:4] (3 items) contain positive frequencies
    #       a[4:8] (4 items) contain negative frequencies
    #    If n=7, n/2=3.5 and n//2 == 3:
    #       a[0] = zero-frequency
    #       a[1:4] (3 items) = positive frequencies (empirically)
    #       a[5:7] (3 items) = negative frequencies (empirically)
    #       so zero and positive is given by a[:n // 2 + 1]
    #    So we select out the zero/positive frequency terms with a[:n/2]
    # 2. Decibel convention is 20 * log_10(x) = 10 * log_10(x^2)

    n = len(time_series)
    fftout = fftpack.fft(time_series)  # alternative: np.fft.fft
    num_zero_and_pos_freqs = int(np.ceil(n / 2))
    if debug:
        log.debug("fft_x_y:\n" + pprint.pformat({
            'n': n,
            'num_zero_and_pos_freqs': num_zero_and_pos_freqs,
        }))
    nyquist_freq_hz = sampling_freq_hz / 2
    x_freq_hz = np.linspace(0.0, nyquist_freq_hz, num=num_zero_and_pos_freqs)
    zero_and_pos_freqs = fftout[:num_zero_and_pos_freqs]
    y_power_db = 2.0 * np.log10(np.abs(zero_and_pos_freqs))  # type: np.ndarray
    return x_freq_hz, y_power_db

    # See also:
    # http://www.gaussianwaves.com/2015/11/interpreting-fft-results-complex-dft-frequency-bins-and-fftshift/  # noqa


def filter_time_series(time_series: np.ndarray,
                       numtaps: int,
                       sampling_freq_hz: float,
                       low_cutoff_hz: float,
                       high_cutoff_hz: float,
                       show_filter_response: bool = False,
                       show_plot: bool = False,
                       log_freq_in_spectrum: bool = True,
                       debug: bool = False) -> np.ndarray:
    filter_taps = make_filter(numtaps=numtaps,
                              sampling_freq_hz=sampling_freq_hz,
                              low_cutoff_hz=low_cutoff_hz,
                              high_cutoff_hz=high_cutoff_hz,
                              show_plot=show_filter_response)
    x, y = x_y_from_coordinates(time_series)
    filtered_y = signal.lfilter(b=filter_taps, a=[1], x=y)
    if debug:
        log.debug("filter_time_series:\n" + pprint.pformat({
            'x': x,
            'y': y,
            'filtered_y': filtered_y,
        }))
    if show_plot:
        fig = plt.figure()
        # noinspection PyPep8
        fig.suptitle(
            "Original time series [sampled/interpolated at {s} Hz]\n"
            "→ filtered [bandpass with half-amplitudes at {l}-{h} Hz]".format(
                s=sampling_freq_hz, l=low_cutoff_hz, h=high_cutoff_hz))

        # Note that pyplot has the concept of "current figure"; see e.g.
        # source to subplot2grid, which calls gcf().

        figshape = (4, 2)  # rows, cols [and similarly, loc is (row, col)]

        ax_orig_sig = plt.subplot2grid(shape=figshape, loc=(0, 0), colspan=2)
        ax_orig_sig.set_title("Original time series")
        ax_orig_sig.set_xlabel("Time (s)")
        ax_orig_sig.set_ylabel("Value")
        ax_orig_sig.plot(x, y, 'k-')
        ax_orig_sig.plot(x, y, 'ro')

        ax_filt_sig = plt.subplot2grid(shape=figshape, loc=(1, 0), colspan=2)
        ax_filt_sig.set_title("Filtered time series")
        ax_filt_sig.set_xlabel("Time (s)")
        ax_filt_sig.set_ylabel("Value")
        ax_filt_sig.plot(x, filtered_y, 'k-')
        ax_filt_sig.plot(x, filtered_y, 'ro')

        ax_orig_spec = plt.subplot2grid(shape=figshape, loc=(2, 0))
        ax_orig_spec.set_title("Original spectrogram")
        ax_orig_spec.set_xlabel("Time (s)")
        ax_orig_spec.set_ylabel("Frequency (Hz)")
        if log_freq_in_spectrum:
            ax_orig_spec.set_yscale('log')
        f_orig, t_orig, spec_orig = signal.spectrogram(y, sampling_freq_hz)
        ax_orig_spec.pcolormesh(t_orig, f_orig, spec_orig)

        ax_filt_spec = plt.subplot2grid(shape=figshape, loc=(3, 0))
        ax_filt_spec.set_title("Filtered spectrogram")
        ax_filt_spec.set_xlabel("Time (s)")
        ax_filt_spec.set_ylabel("Frequency (Hz)")
        if log_freq_in_spectrum:
            ax_filt_spec.set_yscale('log')
        f_filt, t_filt, spec_filt = signal.spectrogram(filtered_y,
                                                       sampling_freq_hz)
        ax_filt_spec.pcolormesh(t_filt, f_filt, spec_filt)

        # http://stackoverflow.com/questions/25735153/plotting-a-fast-fourier-transform-in-python  # noqa
        # http://stackoverflow.com/questions/1523814/units-of-a-fourier-transform-fft-when-doing-spectral-analysis-of-a-signal  # noqa

        ax_orig_fft = plt.subplot2grid(shape=figshape, loc=(2, 1))
        ax_orig_fft.set_title("Original spectrum")
        ax_orig_fft.set_xlabel("Frequency (Hz)")
        if log_freq_in_spectrum:
            ax_orig_fft.set_xscale('log')
        ax_orig_fft.set_ylabel("Power (dB)")
        ax_orig_fft.plot(*fft_x_y(y, sampling_freq_hz=sampling_freq_hz))

        ax_filt_fft = plt.subplot2grid(shape=figshape, loc=(3, 1))
        ax_filt_fft.set_title("Filtered spectrum")
        ax_filt_fft.set_xlabel("Frequency (Hz)")
        if log_freq_in_spectrum:
            ax_filt_fft.set_xscale('log')
        ax_filt_fft.set_ylabel("Power (dB)")
        ax_filt_fft.plot(*fft_x_y(filtered_y,
                                  sampling_freq_hz=sampling_freq_hz))

        plt.show()

    return coordinates_from_x_y(x, filtered_y)


def plot_filter_response(filter_taps: np.ndarray,
                         sampling_freq_hz: float,
                         low_cutoff_hz: float,
                         high_cutoff_hz: float) -> None:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.freqz.html  # noqa
    # http://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units  # noqa
    w, h = signal.freqz(filter_taps)
    fig = plt.figure()

    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_title("Digital filter frequency response")
    ax1.grid()
    ax1.plot(w, 20 * np.log10(np.absolute(h)), 'b')
    ax1.set_ylabel("Amplitude [dB]", color='b')
    ax1.set_xlabel("Normalized frequency [rad/sample]")
    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(h))
    ax2.plot(w, angles, 'g')
    ax2.set_ylabel("Angle (radians)", color='g')

    ax3 = fig.add_subplot(2, 1, 2)
    ax3.grid()
    ax3.set_ylabel("Amplitude", color='b')
    ax3.plot(low_cutoff_hz, 0.5, 'ko')
    ax3.axvline(low_cutoff_hz, color='k')
    ax3.plot(high_cutoff_hz, 0.5, 'ko')
    ax3.axvline(high_cutoff_hz, color='k')
    ax3.plot(0.5 * sampling_freq_hz * w / np.pi, np.abs(h), 'b')
    ax3.set_xlim(0, 0.5 * sampling_freq_hz)
    ax3.set_xlabel("Frequency (Hz)")

    plt.autoscale(enable=True, tight=True)
    plt.show()
