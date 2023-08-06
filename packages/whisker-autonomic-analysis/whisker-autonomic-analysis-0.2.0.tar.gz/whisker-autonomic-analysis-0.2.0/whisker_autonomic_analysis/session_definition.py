#!/usr/bin/env python
# whisker_autonomic_analysis/session_definition.py

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

from datetime import datetime
import tkinter
import tkinter.filedialog
import tkinter.messagebox

from cardinal_pythonlib.reprfunc import auto_repr

from .gui import tkinter_guard_invisible_root


class SessionDefinition(object):
    def __init__(self,
                 date_time: datetime,
                 subject: str,
                 box: int,
                 peakfile_base_dir: str,
                 chunk_duration_s: float) -> None:
        assert date_time is not None
        assert subject
        assert box is not None
        assert chunk_duration_s > 0
        self.date_time = date_time  # part of database PK
        self.subject = subject  # part of database PK
        self.box = box  # part of database PK
        self.peakfile_base_dir = peakfile_base_dir
        self.chunk_duration_s = chunk_duration_s

    def get_peak_filename(self) -> str:
        # Ask the user!
        with tkinter_guard_invisible_root() as _:
            subject_details = "subject {s}, {dt}, box {b}".format(
                s=repr(self.subject),
                dt=self.date_time.strftime("%Y-%m-%d"),  # e.g. 2001-12-31
                b=self.box,
            )
            opentitle = "Open Spike 'peak' data file for " + subject_details
            happy = False
            filename = ''  # make type checker happy too
            while not happy:
                maybe_abort_entirely = False
                filename = tkinter.filedialog.askopenfilename(
                    initialdir=self.peakfile_base_dir,
                    title=opentitle,
                    filetypes=(('All files', '*'),
                               ('Text files', '*.txt'))
                )
                if filename:
                    result = tkinter.messagebox.askyesnocancel(
                        title="Confirm choice of Spike data file",
                        message="Use {f} for {d}?".format(f=repr(filename),
                                                          d=subject_details)
                    )
                    if result is None:  # Cancel
                        maybe_abort_entirely = True
                    elif result:  # Yes
                        happy = True
                    else:  # No
                        pass  # happy remains False
                else:
                    # No filename
                    maybe_abort_entirely = True
                    # and happy remains False
                if maybe_abort_entirely:
                    retry = tkinter.messagebox.askretrycancel(
                        title="Retry, or cancel and quit?",
                        message="Retry choosing file, or cancel "
                                "program entirely?"
                    )  # type: bool
                    if not retry:
                        raise ValueError("User aborted program")
        return filename

    def __repr__(self) -> str:
        return auto_repr(self)

    def __str__(self) -> str:
        return "SessionDefinition(subject={s}, date_time={d}, box={b})".format(
            s=repr(self.subject),
            d=self.date_time.isoformat(),
            b=self.box,
        )
