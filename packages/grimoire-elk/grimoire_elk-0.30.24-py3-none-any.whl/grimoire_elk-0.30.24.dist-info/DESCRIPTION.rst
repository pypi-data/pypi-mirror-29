Welcome to GrimoireELK |Build Status|
=====================================

GrimoireELK is an evolving prototype of the *Grimoire Open Development
Analytics platform*.

Tutorials on howto use it are published in `GrimoireLab
Tutorial <https://grimoirelab.gitbooks.io/tutorial>`__.

Packages
--------

The following packages are produced from this repository:

-  ``grimoire-elk``: |PyPI version|

-  ``grimoire-kidash``: |PyPI version|

``grimoire-elk`` admits some extras, when installing: ``arthur`` (for
installing also ``grimoirelab-arthur`` package) and ``sortinghat`` (for
installing also ``sortinghat`` package). You can specify that you want
to install those extras as follows:

::

    % pip install "grimoire-elk[sortinghat]"
    % pip install "grimoire-elk[arthur]"

.. |Build Status| image:: https://travis-ci.org/grimoirelab/GrimoireELK.svg?branch=master
   :target: https://travis-ci.org/grimoirelab/GrimoireELK
.. |PyPI version| image:: https://badge.fury.io/py/grimoire-elk.svg
   :target: https://badge.fury.io/py/grimoire-elk
.. |PyPI version| image:: https://badge.fury.io/py/grimoire-kidash.svg
   :target: https://badge.fury.io/py/grimoire-kidash


