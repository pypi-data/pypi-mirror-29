
Main features of the fluiddyn package
=====================================

We here give an overview of the main features of the package. Fluiddyn
contains pure python code useful when developing and using fluiddyn
packages. It is like the Ali Baba's cave of the fluiddyn project. Here,
we just show typical import commands and point towards pages in the
documentation.

Just importing the main package can be useful:

.. code:: ipython3

    import fluiddyn as fld

.. code:: ipython3

    fld.constants.g




.. parsed-literal::

    9.81



.. code:: ipython3

    fld.time_as_str()




.. parsed-literal::

    '2018-03-09_11-05-52'



.. code:: ipython3

    fld.get_memory_usage()




.. parsed-literal::

    66.875



.. code:: ipython3

    fld.ipydebug




.. parsed-literal::

    <function fluiddyn.util.util.ipydebug>



is a function to debug code with ipython (simpler than with pdb or ipdb):

Subpackage ``fluiddyn.output``
------------------------------

The subpackage :mod:`fluiddyn.output` ("scientific outputs" like figures and movies) uses (and imports) matplotlib.

.. code:: ipython3

    from fluiddyn.output import show, set_rcparams, gradient_colors

Subpackage ``fluiddyn.io``
--------------------------

The subpackage :mod:`fluiddyn.io` ("input/output") contains modules to save and load data in many formats:

.. code:: ipython3

    from fluiddyn.io import (
        binary, txt, mycsv, hdf5, digiflow, dantec, davis, multitiff, in_py, image)

.. code:: ipython3

    from fluiddyn.io.query import query_yes_no, query, query_number
    from fluiddyn.io.tee import MultiFile

There is also a function to disable the standard output which we use a
lot in unittests.

.. code:: ipython3

    from fluiddyn.io import stdout_redirected

fluiddump
~~~~~~~~~

This package also contains the code of a very simple utility to dump
hdf5 and netcdf files (without dependency in the netcdf library and in
the program ``h5dump``)

.. code:: ipython3

    from fluiddyn.io.dump import dump_h5_file, dump_nc_file

.. code:: ipython3

    ! fluiddump -h


.. parsed-literal::

    usage: fluiddump [-h] [-pv] file
    
    Utility to print the hierarchy of hdf5 and netcdf files.
    
    positional arguments:
      file                  str indicating which file has to be dump.
    
    optional arguments:
      -h, --help            show this help message and exit
      -pv, --print-variables
                            also print the content of the variables


Subpackage ``fluiddyn.util``
----------------------------

The subpackage :mod:`fluiddyn.util` contains functions and modules to do very different things:

.. code:: ipython3

    from fluiddyn.util import (
        time_as_str, get_memory_usage, print_memory_usage,
        import_class, is_run_from_ipython)
    
    # very simple use of mpi (no dependency on mpi4py if the process is run without mpi)
    from fluiddyn.util import mpi
    
    # storing parameters
    from fluiddyn.util.paramcontainer import ParamContainer
    from fluiddyn.util.paramcontainer_gui import QtParamContainer
    
    # handling series of arrays in files
    from fluiddyn.util.serieofarrays import SerieOfArraysFromFiles, SeriesOfArrays
    
    # "tickers"
    from fluiddyn.util.timer import Timer, TimerIrregular
    
    # daemon
    from fluiddyn.util.daemons import DaemonThread, DaemonProcess
    
    # emails
    from fluiddyn.util import mail
    
    # logging
    from fluiddyn.util.logger import Logger
    from fluiddyn.util import terminal_colors
    from fluiddyn.util import config_logging
    
    # matlab to py (command line utility fluidmat2py)
    from fluiddyn.util.matlab2py import cleanmat, mat2wrongpy

fluidinfo: gather information on your Python environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    from fluiddyn.util import info

.. code:: ipython3

    !fluidinfo -h


.. parsed-literal::

    usage: fluidinfo [-h] [-s] [-o OUTPUT_DIR] [-v] [-W]
    
    Displays all important information related to software and hardware. It also
    includes detailed information such as currently installed FluidDyn packages,
    other third-party packages, C compiler, MPI and NumPy configuration.
    
    Examples
    --------
    >>> fluidinfo  # print package, Python, software and hardware info
    >>> fluidinfo -v  # also print basic Numpy info
    >>> fluidinfo -vv  # also print detailed Numpy info
    >>> fluidinfo -s  # save all information into sys_info.xml
    >>> fluidinfo -o /tmp  # save all information into /tmp/sys_info.xml
    
    optional arguments:
      -h, --help            show this help message and exit
      -s, --save            saves system information to an xml file (sys_info.xml)
      -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                            save to directory
      -v, --verbosity       increase output verbosity (max: -vvv)
      -W, --warnings        show warnings


Subpackage ``fluiddyn.calcul``
------------------------------

The subpackage :mod:`fluiddyn.calcul` provides helpers for simple numerical computing.

.. code:: ipython3

    from fluiddyn.calcul import easypyfft

.. code:: ipython3

    from fluiddyn.calcul import sphericalharmo

.. code:: ipython3

    from fluiddyn.calcul import signal

.. code:: ipython3

    from fluiddyn.calcul.setofvariables import SetOfVariables

Subpackage ``fluiddyn.clusters``
--------------------------------

The subpackage :mod:`fluiddyn.clusters` provides classes helping to use computer clusters.

.. code:: ipython3

    from fluiddyn.clusters.legi import Calcul8 as Cluster
    Cluster.print_doc_commands()


.. parsed-literal::

    
    Useful commands
    ---------------
    oarsub -S script.sh
    oarstat -u
    oardel $JOB_ID
    oarsub -C $JOB_ID


.. code:: ipython3

    from fluiddyn.clusters.cines import Occigen as Cluster
    Cluster.print_doc_commands()


.. parsed-literal::

    
    Useful commands
    ---------------
    
    sbatch
    squeue -u $USER
    scancel
    scontrol hold
    scontrol release


Package ``fluiddoc``: helping to build nice web documentations
--------------------------------------------------------------

.. code:: ipython3

    import fluiddoc
    print(fluiddoc.on_rtd)


.. parsed-literal::

    None


.. code:: ipython3

    fluiddoc.mock_modules




.. parsed-literal::

    <function fluiddoc.mock_modules>



.. code:: ipython3

    from fluiddoc.ipynb_maker import ipynb_to_rst
