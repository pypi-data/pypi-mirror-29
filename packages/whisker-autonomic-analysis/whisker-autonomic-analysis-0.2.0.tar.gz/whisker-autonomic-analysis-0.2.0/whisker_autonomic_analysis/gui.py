#!/usr/bin/env python
# whisker_autonomic_analysis/debugging.py

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

import contextlib
import tkinter
from typing import Generator


@contextlib.contextmanager
def tkinter_guard_invisible_root() -> Generator[tkinter.Tk, None, None]:
    """
    1. To use simple tkinter dialog boxes, we don't want a root window visible.
       ... requires tkroot.withdraw()
    2. When simple dialog boxes are finished, they can stay on-screen unless
       you call tkroot.update().
    3. To use matplotlib, we usually don't want a Tk window in existence.
       ... requires tkroot.destroy()

    Therefore, guard simple tkinter use with:

        with tkinter_guard_invisible_root() as _:
            filename = tkinter.askopenfilename(...)

    etc.
    """
    tkroot = tkinter.Tk()  # this has consequences; INTERACTS with pyplot
    # ... so complete and destroy Tkinter windows before returning
    tkroot.withdraw()  # prevent root window from appearing
    yield tkroot
    tkroot.update()  # http://stackoverflow.com/questions/17575552
    tkroot.destroy()
