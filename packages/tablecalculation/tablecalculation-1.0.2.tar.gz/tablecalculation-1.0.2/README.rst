Project Title
=============

Python library to calculate tables for football and handball

Getting Started
---------------

pip install tablecalculation

Alternatively: copy the tablecalculation package to your project.

Prerequisites
~~~~~~~~~~~~~

Should work with Python 2.7 and up or 3. Possibly other versions
(untested).

Usage
~~~~~

It’s best to see `tablecalculationtest.py <tablecalculationtest.py>`__
for reference.

Basic usage is as follows:

::

            # Handball 3. Liga Herren, Saison 2015/16, 17. Spieltag
            # Create table calculation oject with scope, sports type and mode
            t1 = TableCalculation(TABLE_ALL, SPORTSTYPES.HANDBALL, CALCULATION_MODE_DIRECT_COMPARE)

            # add your matches / fixtures (upto desired match day or all)
            t1.add_match(_Match('DHK Flensborg', 35551, 'SC Magdeburg II', 35561, 41, 23))
            t1.add_match(_Match('SV Meck.-Schwerin', 35651, 'TS Großburgwedel', 35661, 26, 17))
            ...

            tb = t1.get_table()
            # tb is now the sorted table

\_Match may be replaced with your own object but as a minimum requires a
team name and id for both participiants and goals for the home and away
team.

The module supports two modes for calculation:
CALCULATION_MODE_GOAL_DIFFERENCE and CALCULATION_MODE_DIRECT_COMPARE.
The first one uses points, followed by goal difference and then goals
scored as sort order (as used in German Bundesliga for example).

CALCULATION_MODE_DIRECT_COMPARE will first sort by points, then the
result of direct comparison between teams with equal points (often used
in handball for the Spanish La Liga).

Tests
-----

Some tests are supplied and can be run like this:

::

    python -m unittest tablecalculation
    python -m unittest tablecalculation.teampoint

Authors
-------

-  **Marco Wilka** - *Initial work* -
   `marcowilka <https://github.com/marcowilka>`__

License
-------

This project is licensed under the MIT License - see the
`LICENSE.txt <LICENSE.txt>`__ file for details
