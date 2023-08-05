atooms-pt: multi-core / multi-GPU parallel tempering
====================================================

|pypi| |version| |license|

`Parallel
tempering <https://en.wikipedia.org/wiki/Parallel_tempering>`__ is a
simulation method that accelerates sampling of configuration space in
systems with rugged energy landscapes. Applications range from the
simulation of biomolecules to studies of phase transitions in condensed
matter or spin glasses. The key idea is to perform Monte Carlo or
molecular dynamics simulations of independent replicas of the system of
interest at different state conditions (say, temperatures). At regular
time intervals, the states of pairs of replicas are exchanged in a way
that respects detailed balance. By changing state conditions during the
simulation, replicas can overcome energy barriers and sample the
configuration space more efficiently.

Since replicas evolve independently between exchanges, the algorithm is
straightforward to parallelize. ``atooms-pt`` relies on
`mpi4py <http://pythonhosted.org/mpi4py/>`__ to distribute groups of
replicas to multiple CPUs and/or GPUs and it builds on the
`atooms <https://pypi.python.org/pypi/atooms>`__ framework to decouple
the algorithm from the underlying simulation backend. The scalability is
excellent up to several tens of CPUs or GPUs. The preferred simulation
backend is `RUMD <http://rumd.org>`__, a molecular dynamics code running
entirely on GPUs that is very efficient even on small system sizes, say
of a few hundreds particles.

Quick start
-----------

From the command line:

.. code:: shell

    pt.py --steps 10 -T 1.0,0.9,0.8 -e 50000 -i data/kalj.xyz.gz /tmp/output_dir

This will run 10 steps of parallel tempering simulation for three
replicas, starting from the configuration in ``data/kalj.xyz.gz`` and
writing output to ``/tmp/output_dir``. The replicas are simulated at
temperatures 1.0, 0.9 and 0.8 and temperature exchanges are attempted
every 50000 steps of the underlying simulation backend.

The same simulation can be ran from python:

.. code:: python

    from atooms.backends.rumd import Rumd
    from atooms.simulation import Simulation
    from atooms.parallel_tempering import ParallelTempering

    temperatures = [1.0, 0.9, 0.8]

    # Create backends and wrap them as simulation instances
    backend = [Rumd(integrator='nvt', temperature=T) for T in temperatures]
    sim = [Simulation(s) for s in backend]
    pt = ParallelTempering(sim, params=temperatures,
                           output_path='/tmp/output_dir',
                           steps=10, exchange_interval=50000)
    pt.run()

The current implementation targets the RUMD molecular dynamics package,
but any atooms simulation backend (for instance, LAMMPS) should work
just fine.

Requirements
------------

-  `numpy <http://numpy.org>`__
-  `atooms <https://gitlab.info-ufr.univ-montp2.fr/atooms/atooms.git>`__
-  `mpi4py <http://pythonhosted.org/mpi4py/>`__
-  `RUMD <http://rumd.org>`__ (for multi-GPU)

Installation
------------

From the python package index

::

    pip install atooms-pt

From the code repository

::

    git clone https://gitlab.info-ufr.univ-montp2.fr/atooms/parallel_tempering.git
    python setup.py install --home=~

Acknowledgments
---------------

This code was developed in the context of PRACE ("Partnership for
Advanced Computing in Europe") project 2010PA1751 "Multi-GPU parallel
tempering simulations".

Authors
-------

Daniele Coslovich:
http://www.coulomb.univ-montp2.fr/perso/daniele.coslovich/

.. |pypi| image:: https://img.shields.io/pypi/v/atooms-pt.svg
   :target: https://pypi.python.org/pypi/atooms-pt/
.. |version| image:: https://img.shields.io/pypi/pyversions/atooms-pt.svg
   :target: https://pypi.python.org/pypi/atooms-pt/
.. |license| image:: https://img.shields.io/pypi/l/atooms-pt.svg
   :target: https://en.wikipedia.org/wiki/GNU_General_Public_License


