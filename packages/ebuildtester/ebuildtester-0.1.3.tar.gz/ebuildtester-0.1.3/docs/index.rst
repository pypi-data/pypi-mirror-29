.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Introduction
============

This script is a tool to test a Gentoo ebuild and its
dependencies. The idea is that the package is emerged in a clean (and
current) stage3 Docker container.


Usage
-----

We are going to assume that the user has a local git clone of the portage tree in

.. code-block:: bash

   /usr/local/git/gentoo

Then a particular ebuild (ATOM) can be tested with:

.. code-block:: python

   ebuildtester --portage-dir /usr/local/git/gentoo \
     --atom ATOM


Command line arguments
----------------------

The command understands the following command line arguments:

.. code-block:: sh

   usage: ebuildtester [-h] [--atom ATOM [ATOM ...]] [--manual] --portage-dir
                       PORTAGE_DIR [--overlay-dir OVERLAY_DIR] [--update]
                       [--threads N] [--use USE [USE ...]] [--unmask ATOM]
                       [--gcc-version VER] [--with-X]

   optional arguments:
     -h, --help            show this help message and exit
     --atom ATOM [ATOM ...]
                           The package atom(s) to install
     --manual              Install package manually
     --portage-dir PORTAGE_DIR
                           The local portage directory
     --overlay-dir OVERLAY_DIR
                           Add overlay dir (can be used multiple times)
     --update              Update container before installing atom
     --threads N           Use N threads to build packages
     --use USE [USE ...]   The use flags for the atom
     --unmask ATOM         Unmask atom (can be used multiple times)
     --gcc-version VER     Use gcc version VER
     --with-X              Install VNC server to test graphical applications
