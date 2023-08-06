Undertime - pick a meeting time
===============================

This program allows you to quickly pick a meeting time across multiple
timezones for conference calls or other coordinated events. It shows
all times of a given day for all the timezones selected, in a table
that aligns the time so a line shows simultaneous times across all
timezones. This takes into account daylight savings and other
peculiarities (provided that the local timezone database is up to
date) so you can also schedule meetings in the future as well.

.. image:: undertime.png
   :alt: undertime computing possible meeting time for multiple timezones

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg 
   :alt: Say thanks to the author
   :target: https://saythanks.io/to/anarcat

Usage
=====

Timezones should be passed on the commandline and are matched against
the `list of known timezones`_, as defined by the `pytz`_
package. Exact matches are attempted at first, but if that fails,
substring matches are allowed, which makes it possible to do this::

  undertime.py New_York Los_Angeles

The complete list of timezones is also shown when the
``--print-zones`` commandline option is provided.

Colors are used to highlight the "work hours" where possible meeting
times could overlap. You can change those work hours with the
``--start`` and ``--end`` flags. Because daylight savings may actually
change time, you can also use the ``--date`` time to pick an arbitrary
time for the meeting, using natural language (as parsed by the
`parsedatetime`_ library). The current time is also shown, in bold.

Full usage is available with the ``--help`` flag and the
manpage. Instructions for how to contribute to the project are in
``CONTRIBUTING.rst`` and there is a ``CODE_OF_CONDUCT.rst``.

.. _list of known timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
.. _pytz: https://pypi.python.org/pypi/pytz
.. _parsedatetime: https://pypi.python.org/pypi/parsedatetime/
.. _overtime-cli: https://github.com/diit/overtime-cli

Known issues and limitations
============================

There are weird alignment issues when using colors, which seems to be
a bug with the upstream `terminaltables`_ library, filed as `issue
#55`_.

It is possible that daylight saving times computations are
incorrect. There are no unit tests for this program, which was only
manually tested with some commonly used timezones.

Timezones are a delicate and complicated subject, and change
constantly. What may be applicable to your location at the current
time may not be reflected by your operating system or the chain of
software used by this program to determine time.

It should be possible for the program to show the user which are the
best times to possibly do a meeting. Those, for example, could be
outlined in green or underlined to make it more obvious when the best
matches are. Another suggestion that was proposed is to restrict the
display to overlapping timezones (`issue #3`_).

There is no ``--version`` flag because of limitations in Python's
performance, see `issue #4`_ for a full discussion.

Undertime was written using Python 3.5 and there is no garantee it
will work in older Python releases.

.. _terminaltables: https://robpol86.github.io/terminaltables/
.. _issue #55: https://github.com/Robpol86/terminaltables/issues/55
.. _issue #4: https://gitlab.com/anarcat/undertime/issues/3
.. _issue #4: https://gitlab.com/anarcat/undertime/issues/4

Credits
=======

This program was written by Antoine Beaupré and is licensed under the
AGPLv3+. It was inspired by the `overtime-cli`_ program and the
`timeanddate.com`_ site. Another similar tool is `worldchatclock.com`_
and its beautiful round interface.

I rewrote `overtime-cli`_ in Python because I felt we shouldn't need a
Javascript virtual machine to pick a time. I was also curious to see
how such a rewrite would look like and was tired of loading a web
browser every time I needed to figure out what time it was elsewhere
in the world or when I needed to coordinate international meetings.

.. _timeanddate.com: https://www.timeanddate.com/
.. _worldchatclock.com: http://worldchatclock.com/


