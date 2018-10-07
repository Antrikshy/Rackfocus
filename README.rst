Rackfocus
=========

Rackfocus (or rackfocus) is a CLI tool to compile IMDb datasets into a convenient SQLite database for easy consumption.

IMDb provides open access to an assortment of their data for non-commercial use. This data is packaged in TSV files that are available to download without any authentication. See their `Datasets page <https://www.imdb.com/interfaces>`_ for more information.

It might be super nifty for data visualization projects and other similar use cases, but it's hard to "peek" into the data, as it often involves joins. For instance, cast, crew and titles are referred to by unique IDs, and looking up their names requires joining datasets with other datasets. Rackfocus makes it easy to surf through the data (assuming you speak SQL) by compiling it all into a compact SQLite file.

Usage
-----

Requirements
~~~~~~~~~~~~

All that's required to run Rackfocus is Python 3 (I'm pretty certain as low as 3.4 should work, possibly lower). It does not depend on any third-party packages.

Installing + Running
~~~~~~~~~~~~~~~~~~~~

You can find Rackfocus on PyPI using pip::

  pip install rackfocus

That should get you set up with a `rackfocus` command that can be invoked from anywhere like so::

  rackfocus ./path/to/working/dir ./path/to/output/dir

Rackfocus will use the working directory (first argument) to place datasets temporarily. Working data will be contained in a new directory that Rackfocus creates, which will be destroyed after the compilation is complete.

Rackfocus's output is a neat little SQLite database in a file named `rackfocus_out.db`, which is placed under the path specified as the second argument.

Tip - Schedule It!
~~~~~~~~~~~~~~~~~~

During its development, Rackfocus was intended to be scheduled. Say you enjoy data visualization and always want the latest IMDb data ready to dip into. Simply set up the job to run periodically on any computer, perhaps a Raspberry Pi. Use cron or another scheduling mechanism to update data daily or weekly!

The database file that gets generated as output has a reliable, unchanging file name. That way, it gets overwritten when scheduled, without requiring any cleanup.

Data Model
----------

The output SQLite database file includes tables that more or less mirror the TSV files that IMDb provides, with a few quality-of-life joining and browsing enhancements. These enhancements are mainly some extra unpacking of rows into multiple rows.

Much of the data model described on `IMDb's datasets page <https://www.imdb.com/interfaces>`_ applies. Any overrides to this can be deduced from the `rackfocus/models.py` file in this repo.

There are two key facts about the datasets to get you started:

1. `tconst` values represent unique titles. Entities like movies, shorts, video games, TV series, and even individual TV episodes share this namespace.
2. `nconst` values represent unique people.

These values also happen to appear in URLs for people and titles on IMDb. For example, Nicolas Cage is `nm0000115 <https://www.imdb.com/name/nm0000115>`_.

Contributing
------------

Improvements are very welcome, and contributing them is easy! Rackfocus is a very straightforward application, with zero package dependencies outside of Python itself. Simply fork and/or clone this repo and you should be good to go.

From the top-level directory of this repo, run::

  pip install -e .

That should install your local version of Rackfocus in your environment. Run the same command after making each change and it should refresh the local install to reflect changes.

To restore your system to the original state, run::

  pip uninstall rackfocus
