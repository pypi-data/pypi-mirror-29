#!/usr/bin/env python
# whisker_autonomic_analysis/maths.py

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
from typing import Dict, Iterable, Optional, Tuple, Union

import numpy as np

log = logging.getLogger(__name__)

FloatLikeSingle = Union[float, np.float64]
FloatLikeSingleOrVec = Union[FloatLikeSingle, np.ndarray]
ParamDict = Dict[str, Optional[FloatLikeSingle]]


# =============================================================================
# Conversion/arithmetic functions
# =============================================================================

def s_from_ms(values_ms: FloatLikeSingleOrVec) -> FloatLikeSingleOrVec:
    return values_ms / 1000


def ms_from_s(values_s: FloatLikeSingleOrVec) -> FloatLikeSingleOrVec:
    return values_s * 1000


def hr_bpm_from_rr_ms(rr_interval_ms: FloatLikeSingleOrVec) \
        -> FloatLikeSingleOrVec:
    """
    Calculates heart rate (HR) in beats per minute (bpm) from an R-R interval
    in milliseconds.
    """
    return 60 * 1000 / rr_interval_ms


def per_minute_from_freq_hz(freq_hz: FloatLikeSingleOrVec) \
        -> Union[float, np.ndarray]:
    return 60 * freq_hz


def remove_none_from_np_array(a: np.ndarray) -> np.ndarray:
    # http://stackoverflow.com/questions/25254929/efficient-way-of-removing-nones-from-numpy-array  # noqa
    # noinspection PyTypeChecker
    return a[a != np.array(None)]


def mean(values: Union[np.ndarray, Iterable[Optional[FloatLikeSingle]]],
         remove_none: bool = True) -> Optional[FloatLikeSingle]:
    # Note that np.mean() can't cope with None.
    # We could roll our own mean function, but the np ones are fast.
    if not isinstance(values, np.ndarray):
        values = np.array(values)
    if remove_none:
        values = remove_none_from_np_array(values)
    if len(values) == 0:
        return None
    result = np.mean(values)  # type: FloatLikeSingle
    return result


def rms(values: np.ndarray) -> FloatLikeSingle:
    """Root mean square (RMS)."""
    return np.sqrt(np.mean(np.power(values, 2)))


def minus(a: Optional[FloatLikeSingle],
          b: Optional[FloatLikeSingle]) -> Optional[FloatLikeSingle]:
    if a is None or b is None:
        return None
    return a - b


def dictminus(a: ParamDict, b: ParamDict) -> ParamDict:
    result = {}  # type: ParamDict
    for k in a.keys():
        if k in b:
            result[k] = minus(a[k], b[k])
        else:
            result[k] = None
    return result


def to_db_float(x: Optional[FloatLikeSingle]) -> Optional[float]:
    """
    The database is unlikely to handle Python's float('nan'),
    float('-inf'), or float('inf') values, and also SQLAlchemy doesn't have
    default converters for numpy float types like numpy.float64.
    """
    if x is None:
        return None
    if not math.isfinite(x):  # e.g. nan, -inf, +inf
        return None
    return float(x)


# =============================================================================
# Coordinate transformations
# =============================================================================

def coordinates_from_x_y(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    # Array or matrix?
    # http://stackoverflow.com/questions/4151128/what-are-the-differences-between-numpy-arrays-and-matrices-which-one-should-i-u  # noqa
    # ... array
    assert len(x) == len(y)
    coords = np.array(list(zip(x, y)))
    validate_coordinates(coords, dimensions=2)
    return coords
    # looks like: [[x1, y1], [x2, y2], [x3, y3], ...]


def validate_coordinates(coords: np.ndarray, dimensions: int = 2) -> None:
    """
    Coords should be a list of n-tuples, where n is the number of dimensions
    (e.g. 2 for x, y).

    So we index like:
        x = coord[n][0]
        y = coord[n][1]
    """
    rank = coords.ndim
    shape = coords.shape
    assert rank == 2, (
        "Expected rank == 2; got rank={r}; from {c}".format(r=rank, c=coords))
    assert shape[1] == dimensions, (
        "Expected shape[1]={d}; got rank={r}, shape[1]={s}; "
        "from {c}".format(d=dimensions, r=rank, s=shape[1], c=coords))


def x_y_from_coordinates(coords: np.ndarray,
                         debug: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    validate_coordinates(coords, dimensions=2)
    rolled = np.rollaxis(coords, axis=1)
    x = rolled[0]
    y = rolled[1]
    if debug:
        log.debug("x_y_from_coordinates:\n" + pprint.pformat({'coords': coords,
                                                              'rolled': rolled,
                                                              'x': x,
                                                              'y': y}))
    return x, y


def rotation_matrix(theta_degrees: FloatLikeSingle) -> np.matrix:
    """
    Rotation matrix to rotate the x,y plan anticlockwise by theta about
    the origin.

    (To rotate about somewhere else: translate, rotate, un-translate.)
    """
    # http://scipython.com/book/chapter-6-numpy/examples/creating-a-rotation-matrix-in-numpy/  # noqa
    # https://en.wikipedia.org/wiki/Rotation_matrix
    # http://mathforum.org/library/drmath/view/69806.html
    # noinspection PyTypeChecker
    theta_radians = np.radians(theta_degrees)
    c = np.cos(theta_radians)
    s = np.sin(theta_radians)
    r = np.matrix([[c, -s], [s, c]])
    return r


def rotate_coordinates(coords: np.ndarray,
                       rot_matrix: np.matrix,
                       dimensions: int = 2) -> np.ndarray:
    validate_coordinates(coords, dimensions=dimensions)
    return np.asarray(np.dot(coords, rot_matrix.T))
