==============
MPI map
==============

`Documentation <http://mpi-map.readthedocs.io>`_

This package uses `mpi4py <https://pypi.python.org/pypi/mpi4py/>`_ and `dill <http://trac.mystic.cacr.caltech.edu/project/pathos/wiki/dill.html>`_ to spawn processes and execute them.

Installation
============

You need to have an MPI back-end installed on your machine and add the right path on the ``$LD_LIBRARY_PATH``, so that `mpi4py <https://pypi.python.org/pypi/mpi4py/>`_ can link to it. You should install `mpi4py <https://pypi.python.org/pypi/mpi4py/>`_ manually by

   $ pip install mpi4py

When everything is set, you can install the ``mpi_map`` using:

    $ pip install mpi_map

ChangeLog
=========

v1.0.1
------

* map methods of classes

v1.0.3
------

* added export of cwd in order to allow import of local modules

v1.0.17
-------

* Removed disconnect on stop(). This was causing an unnecessary deadlock.

v1.0.18
-------

* Reverted change of 1.0.17. The problem with disconnect seems to be related to mpi4py.

v1.0.19
-------

* Removed disconnect from children. Added free on master.

v1.0.20
-------

* Allowing for the running of method belonging to an object in the distributed memory.

v2.0
----

* Advanced management of distributed memory

v2.1
----

* Fixed a leftover bug on the allocation of memory thorugh function evaluation.

v2.2
----

* Added barrier synchronization to prevent buffer overloading in heavily asynchronous applications

v2.3
----

* Added barrier sync in binary communications

v2.4
----

* Fixed handling of non-tuple outputs in mpi_map_alloc_dmem
