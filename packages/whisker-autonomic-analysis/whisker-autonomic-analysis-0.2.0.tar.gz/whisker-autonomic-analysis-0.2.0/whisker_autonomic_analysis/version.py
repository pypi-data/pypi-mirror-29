#!/usr/bin/env python
# whisker_autonomic_analysis/version.py

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

VERSION = "0.2.0"  # use semantic version system
VERSION_DATE = "2018-03-08"

VERSION_HISTORY = """

- 0.1.4 (2017-03-14): released.

- 0.1.5 (2017-04-11): added facility to process only sessions found in a
  manually curated master table.
  Table name is SessionsForAutonomicAnalysis (q.v.), which needs the same
    - DateTimeCode
    - Subject
    - Box
  columns as the Config table.

- 0.1.6 (2017-04-11): removed one incorrect assertion from
  TrialTiming.__init__()
  
- 0.1.7 (2017-04-29): define CS/US timing from database, rather than hard-coded
  - Added ChunkDurationSec (float) to SessionsForAutonomicAnalysis table.
  - So, creation SQL is:
  
    CREATE TABLE SessionsForAutonomicAnalysis (
        DateTimeCode DATETIME NOT NULL,
        Subject VARCHAR(45) NOT NULL,
        Box INT NOT NULL,
        ChunkDurationSec FLOAT NOT NULL
    );
    
    and a quick population command is:
    
    INSERT INTO SessionsForAutonomicAnalysis (
        DateTimeCode,
        Subject,
        Box,
        ChunkDurationSec
    )
    SELECT
        DateTimeCode,
        Subject,
        Box,
        10.0
    FROM Config;

  - Bugfixes for zero-length slices.

- 0.1.8 (2017-05-01): changed the definition of how baseline/CS are split
  into chunks. See StimulusLockedTelemetry.init().
  
- 0.1.9 (2017-05-04): changes to definition of "baseline" by Laith; see
  aversive_pavlovian_database.py
  
- 0.2.0 (2018-03-08): changes for HFC
    - alternative input formats considered: textual output from old 
      AversivePavlovian code by Katrin. ***
    - whole-session analysis
    - R-R interval output files, as input to Kubios for cross-check
    - cope with the fact that Spike sometimes produces its RRint; see below and
      gen_telemetry()
    - also renamed stimulus_bp.py to main.py
    
EXAMPLE OF SPIKE FILE WITH RR INTERVAL IN MILLISECONDS
e.g. Gozo_Discrim01_27Feb17_peak.txt

#  time	   RR-Int	 Heart Rate	   time	  Systole	   time	  Diastole
      0.242	  344.500	  174.165	    0.414	  176.123	    0.541	  120.947	   0
      0.500	  170.900	  351.083	    0.585	  177.832	    0.710	  120.703	   0

EXAMPLE OF SPIKE FILE WITH RR INTERVAL IN SECONDS
e.g. Parsnip_Cueprobe_21May15_peak.txt

Time	RRint	Heartrate	Time	Systolic	Time	Diastolic
0.025600	0.025600	2343.750000	0.025600	149.496460	0.188780	104.180908
0.231680	0.206080	291.149068	0.231680	150.042725	0.388290	105.752563

"""
