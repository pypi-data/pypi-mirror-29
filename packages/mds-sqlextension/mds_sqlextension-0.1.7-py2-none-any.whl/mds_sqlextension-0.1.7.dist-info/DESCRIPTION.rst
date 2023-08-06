sqlextension
============
This module makes some SQL commands available for use with python-sql.

Install
=======
pip install mds-sqlextension

Available SQL functions
=======================

- AnyInArray (any)
- ArrayAgg (array_agg)
- Ascii (ascii)
- Concat2 (concat)
- FuzzyEqal (%)
- Lower (lower)
- Replace (replace)
- ReplaceRegexp (regexp_replace)
- RPad (rpad)
- SplitPart (split_part)
- StringAgg (string_agg)

Available SQL expressions
=========================

- Overlaps ( (start1, end1) overlaps (start2, end2) )::

    tab1.select(
       tab1.id, 
       where=Overlaps('2017-10-01', '2017-10-15', tab1.start, tab1.end) == True
       )

To make FuzzyEqual work, call *CREATE EXTENSION pg_trgm;* in PostgreSQL.

Requires
========
- python-sql

Changes
=======

*0.1.7 - 03/09/2018*

- fix: generate valid params in 'Overlaps'

*0.1.6 - 03/08/2018*

- added expression: Overlaps

*0.1.5 - 02/01/2018*

- added function: ReplaceRegexp

*0.1.4 - 12/14/2017*

- bugfix: import-syntax in python3
- added docstrings for help

*0.1.3 - 07/14/2017*

- added 'split_part'

*0.1.2 - 06/09/2017*

- import optimized

*0.1.1 - 06/09/2017*

- first public version


