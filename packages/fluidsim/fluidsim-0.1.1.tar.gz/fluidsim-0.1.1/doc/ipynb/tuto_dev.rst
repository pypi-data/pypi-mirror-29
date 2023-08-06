
.. code:: ipython3

    from __future__ import print_function
    %matplotlib inline

.. _tutosimuldev:

Tutorial: understand how FluidSim works
=======================================

A goal of FluidSim is to be as simple as possible to allow anyone knowing a little bit of Python to understand how it works internally. For this tutorial, it is assumed that the reader knows how to run simulations with FluidSim. If it is not the case, first read the tutorial `running a simulation (user perspective) <tuto_user.html>`_.

A class to organize parameters
------------------------------

First, we need to present the important class `fluiddyn.util.paramcontainer.ParamContainer <http://fluiddyn.readthedocs.org/en/latest/generated/fluiddyn.util.paramcontainer.html>`_ used to contain information.

.. code:: ipython3

    from fluiddyn.util.paramcontainer import ParamContainer
    params = ParamContainer(tag='params')
    params._set_attribs({'a0': 1, 'a1': 1})
    params._set_attrib('a2', 1)
    params._set_child('child0', {'a0': 1})
    params.a2 = 2
    params.child0.a0 = 'other option'


.. parsed-literal::

    /home/pierre/opt/miniconda3/envs/latest/lib/python3.6/site-packages/h5py/__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
      from ._conv import register_converters as _register_converters


A ``ParamContainer`` can be represented as xml

.. code:: ipython3

    params




.. parsed-literal::

    <fluiddyn.util.paramcontainer.ParamContainer object at 0x7fe0629984a8>
    
    <params a0="1" a1="1" a2="2">
      <child0 a0="other option"/>  
    
    </params>



FluidSim uses instances of this class to store the information of a
particular solver and the parameters of a particular simulation.

The Simul classes and the default parameters
--------------------------------------------

The first step to run a simulation is to import a Simul class from a
solver module, for example:

.. code:: ipython3

    from fluidsim.solvers.ns2d.solver import Simul

Any solver module has to define a class called Simul which has to have
some important attributes:

.. code:: ipython3

    [name for name in dir(Simul) if not name.startswith('__')]




.. parsed-literal::

    ['InfoSolver',
     '_complete_params_with_default',
     'compute_freq_diss',
     'create_default_params',
     'tendencies_nonlin']



The first attribute :class:`InfoSolver` is a class deriving from :class:`ParamContainer`. This class is usually defined in the `solver` module. It is used during the instantiation of the Simul object to produce a :class:`ParamContainer` containing a description of the solver, in practice the names and the modules of the classes used for the different tasks that need to be performed during the simulation.

There are also four other functions. :func:`compute_freq_diss` and :func:`tendencies_nonlin` are used during the simulation and describe the equations that are solved.

:func:`create_default_params` and :func:`_complete_params_with_default` are used to produce the `ParamContainer` containing the default parameters for a simulation:

.. code:: ipython3

    params = Simul.create_default_params()

During the creation of `params`, the class :class:`InfoSolver` has been used to create a :class:`ParamContainer` named `info_solver`:

.. code:: ipython3

    Simul.info_solver




.. parsed-literal::

    <fluidsim.solvers.ns2d.solver.InfoSolverNS2D object at 0x7fe0629849b0>
    
    <solver class_name="Simul" module_name="fluidsim.solvers.ns2d.solver"
            short_name="NS2D">
      <classes>
        <Operators class_name="OperatorsPseudoSpectral2D"
                   module_name="fluidsim.operators.operators2d"/>  
    
        <State class_name="StateNS2D" keys_computable="[]"
               keys_linear_eigenmodes="['rot_fft']" keys_phys_needed="['rot']"
               keys_state_phys="['ux', 'uy', 'rot']" keys_state_spect="['rot_fft']"
               module_name="fluidsim.solvers.ns2d.state"/>  
    
        <TimeStepping class_name="TimeSteppingPseudoSpectral"
                      module_name="fluidsim.base.time_stepping.pseudo_spect_cy"/>  
    
        <InitFields class_name="InitFieldsNS2D"
                    module_name="fluidsim.solvers.ns2d.init_fields">
          <classes>
            <from_file class_name="InitFieldsFromFile"
                       module_name="fluidsim.base.init_fields"/>  
    
            <from_simul class_name="InitFieldsFromSimul"
                        module_name="fluidsim.base.init_fields"/>  
    
            <in_script class_name="InitFieldsInScript"
                       module_name="fluidsim.base.init_fields"/>  
    
            <constant class_name="InitFieldsConstant"
                      module_name="fluidsim.base.init_fields"/>  
    
            <noise class_name="InitFieldsNoise"
                   module_name="fluidsim.solvers.ns2d.init_fields"/>  
    
            <jet class_name="InitFieldsJet"
                 module_name="fluidsim.solvers.ns2d.init_fields"/>  
    
            <dipole class_name="InitFieldsDipole"
                    module_name="fluidsim.solvers.ns2d.init_fields"/>  
    
          </classes>
    
        </InitFields>
    
        <Forcing class_name="ForcingNS2D"
                 module_name="fluidsim.solvers.ns2d.forcing">
          <classes>
            <in_script class_name="InScriptForcingPseudoSpectral"
                       module_name="fluidsim.base.forcing.specific"/>  
    
            <proportional class_name="Proportional"
                          module_name="fluidsim.base.forcing.specific"/>  
    
            <tcrandom class_name="TimeCorrelatedRandomPseudoSpectral"
                      module_name="fluidsim.base.forcing.specific"/>  
    
            <tcrandom_anisotropic
                                  class_name="TimeCorrelatedRandomPseudoSpectralAnisotropic"
                                  module_name="fluidsim.base.forcing.specific"/>  
    
          </classes>
    
        </Forcing>
    
        <Output class_name="Output" module_name="fluidsim.solvers.ns2d.output">
          <classes>
            <PrintStdOut class_name="PrintStdOutNS2D"
                         module_name="fluidsim.solvers.ns2d.output.print_stdout"/>  
    
            <PhysFields class_name="PhysFieldsBase2D"
                        module_name="fluidsim.base.output.phys_fields"/>  
    
            <Spectra class_name="SpectraNS2D"
                     module_name="fluidsim.solvers.ns2d.output.spectra"/>  
    
            <spatial_means class_name="SpatialMeansNS2D"
                           module_name="fluidsim.solvers.ns2d.output.spatial_means"/>  
    
            <spect_energy_budg class_name="SpectralEnergyBudgetNS2D"
                               module_name="fluidsim.solvers.ns2d.output.spect_energy_budget"/>  
    
            <increments class_name="Increments"
                        module_name="fluidsim.base.output.increments"/>  
    
          </classes>
    
        </Output>
    
        <Preprocess class_name="PreprocessPseudoSpectral"
                    module_name="fluidsim.base.preprocess.pseudo_spect">
          <classes/>  
    
        </Preprocess>
    
      </classes>
    
    </solver>



We see that this solver uses many classes and that they are organized in tasks ("Operator", "InitFields", "TimeStepping", "State", "Output", "Forcing"). Some first-level classes (for example "Output") have second-level classes ("PrintStdOut", "Spectra", "PhysFields", etc.). Such description of a solver is very general. It is also very conveniant to create a new solver from a similar existing solver.

Every classes can have a class function or a static function :func:`_complete_params_with_default` that is called when the object containing the default parameters is created.

The objects `params` and `Simul.info_solver` are then used to instantiate the simulation (here with the default parameters for the solver):

.. code:: ipython3

    sim = Simul(params)


.. parsed-literal::

    *************************************
    Program fluidsim
    sim:                <class 'fluidsim.solvers.ns2d.solver.Simul'>
    sim.oper:           <class 'fluidsim.operators.operators2d.OperatorsPseudoSpectral2D'>
    sim.output:         <class 'fluidsim.solvers.ns2d.output.Output'>
    sim.state:          <class 'fluidsim.solvers.ns2d.state.StateNS2D'>
    sim.time_stepping:  <class 'fluidsim.base.time_stepping.pseudo_spect_cy.TimeSteppingPseudoSpectral'>
    sim.init_fields:    <class 'fluidsim.solvers.ns2d.init_fields.InitFieldsNS2D'>
    
    solver NS2D, RK4 and sequential,
    type fft: fluidfft.fft2d.with_pyfftw
    nx =     48 ; ny =     48
    lx = 8 ; ly = 8
    path_run =
    /home/pierre/Sim_data/NS2D_48x48_S8x8_2018-03-14_07-58-47
    init_fields.type: constant
    
    Initialization outputs:
    sim.output.phys_fields:       <class 'fluidsim.base.output.phys_fields.PhysFieldsBase2D'>
    sim.output.spectra:           <class 'fluidsim.solvers.ns2d.output.spectra.SpectraNS2D'>
    sim.output.increments:        <class 'fluidsim.base.output.increments.Increments'>
    sim.output.spatial_means:     <class 'fluidsim.solvers.ns2d.output.spatial_means.SpatialMeansNS2D'>
    sim.output.spect_energy_budg: <class 'fluidsim.solvers.ns2d.output.spect_energy_budget.SpectralEnergyBudgetNS2D'>
    
    Memory usage at the end of init. (equiv. seq.): 98.0546875 Mo
    Size of state_spect (equiv. seq.): 0.0192 Mo


Let’s print the attributes of ``sim`` that are not class attributes:

.. code:: ipython3

    [name for name in dir(sim) if not name.startswith('_') and name not in dir(Simul)]




.. parsed-literal::

    ['info',
     'init_fields',
     'is_forcing_enabled',
     'name_run',
     'oper',
     'output',
     'params',
     'preprocess',
     'state',
     'time_stepping']



Except ``name_run`` and ``info``, the attributes are instances of the
first-level classes defined in ``Simul.info_solver``. These different
objects have to interact together. We are going to present these
different hierarchies of classes but first we come back to the two
functions describing the equations in a pseudo-spectral solver.

Description of the solved equations
-----------------------------------

The functions :func:`Simul.compute_freq_diss` and :func:`Simul.tendencies_nonlin` define the solved equations. Looking at the documentation of the solver module :mod:`fluidsim.solvers.ns2d.solver`, we see that :func:`Simul.tendencies_nonlin` is defined in this module and that :func:`Simul.compute_freq_diss` is inherited from the base class :class:`fluidsim.base.solvers.pseudo_spect.SimulBasePseudoSpectral`. By clicking on these links, you can look at the documentation and the sources of these functions. The documentation explains how this function define the solved equations. I think the sources are quite clear and can be understood by anyone knowing a little bit of Python for science. Most of the objects involved in these functions are functions or numpy.ndarray_.

.. _numpy.ndarray: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html

State classes (``sim.state``)
-----------------------------

`sim.state` is an instance of :class:`fluidsim.solvers.ns2d.state.StateNS2D`. It contains numpy.ndarray_, actually slightly modified numpy.ndarray_ named :class:`fluidsim.base.setofvariables.SetOfVariables`. This class is used to stack variables together in a single numpy.ndarray_.

The state classes are also able to compute other variables from the state of the simulation. It is an interface hidding the actual way the data are stored.

Operator classes (``sim.oper``)
-------------------------------

`sim.oper` is an instance of :class:`fluidsim.operators.operators.OperatorsPseudoSpectral2D`.

It contains the information on the grids (in physical and spectral space) and provides many optimized functions on arrays representing fields on these grids.

It has to be fast! For the two dimensional Fourier pseudo-spectral solvers, it is written in Cython.

TimeStepping classes (``sim.time_stepping``)
--------------------------------------------

`sim.time_stepping` is an instance of :class:`fluidsim.base.time_stepping.pseudo_spect_cy.TimeSteppingPseudoSpectral`, which is based on :class:`fluidsim.base.time_stepping.pseudo_spect.TimeSteppingPseudoSpectral` and :class:`fluidsim.base.time_stepping.base.TimeSteppingBase`.

This class contains the functions for the time advancement, i.e. Runge-Kutta functions and the actual loop than increments the time stepping index `sim.time_stepping.it`. The Runge-Kutta functions call the function :func:`sim.tendencies_nonlin` and modify the state in Fourier space `sim.state.state_fft`.

The loop function also call the function :func:`sim.output.one_time_step`.

Output classes (``sim.output``)
-------------------------------

`sim.output` is an instance of :class:`fluidsim.solvers.ns2d.output.Output`.

Saving and plotting of online or on-the-fly postprocessed data - i.e., data generated by processing the solver state variables at regular intervals during simulation time. It could include physical fields, spatially averaged means, spectral energy budgets, PDFs etc.

Forcing classes (``sim.forcing``)
---------------------------------

`sim.forcing` is an instance of :class:`fluidsim.solvers.ns2d.forcing.ForcingNS2D`.

If `params.forcing.enable` is True, it is used in :func:`sim.tendencies_nonlin` to add the forcing term.
