***************
Release Notes
***************

timeboard 0.1
=============

**Release date:** February 01, 2018

This is the first release.


timeboard 0.1.1
===============

**Release date:** March 01, 2018

New features
------------

* :py:meth:`.Interval.overlap` (also ``*``) - return the interval that is the intersection of two intervals.

* :py:meth:`.Interval.what_portion_of` (also ``/``) - calculate what portion of the other interval this interval takes up.

* :py:meth:`.Interval.workshifts` - return the generator that yields workshifts with the specified duty.

* Work time calculation: :py:meth:`.Workshift.worktime`, :py:meth:`.Interval.worktime`

Miscellaneous
-------------

* Performance: any practical timeboard should take at the most one second to build.

* Documentation: added "Common Use Cases" section and the notebook.
