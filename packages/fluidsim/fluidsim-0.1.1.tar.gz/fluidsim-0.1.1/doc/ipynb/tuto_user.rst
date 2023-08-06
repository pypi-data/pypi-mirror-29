
.. code:: ipython3

    from __future__ import print_function
    %matplotlib inline
    import fluidsim


.. parsed-literal::

    /home/pierre/opt/miniconda3/envs/latest/lib/python3.6/site-packages/h5py/__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
      from ._conv import register_converters as _register_converters


.. _tutosimuluser:

Tutorial: running a simulation (user perspective)
=================================================

In this tutorial, I’m going to show how to run a simple simulation with
a solver that solves the 2 dimensional Navier-Stokes equations. I’m also
going to present some useful concepts and objects used in FluidSim.

A minimal simulation
--------------------

Fisrt, let’s see what is needed to run a very simple simulation. For the
initialization (with default parameters):

.. code:: ipython3

    from fluidsim.solvers.ns2d.solver import Simul
    params = Simul.create_default_params()
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
    /home/pierre/Sim_data/NS2D_48x48_S8x8_2018-03-14_07-58-29
    init_fields.type: constant
    
    Initialization outputs:
    sim.output.phys_fields:       <class 'fluidsim.base.output.phys_fields.PhysFieldsBase2D'>
    sim.output.spectra:           <class 'fluidsim.solvers.ns2d.output.spectra.SpectraNS2D'>
    sim.output.increments:        <class 'fluidsim.base.output.increments.Increments'>
    sim.output.spatial_means:     <class 'fluidsim.solvers.ns2d.output.spatial_means.SpatialMeansNS2D'>
    sim.output.spect_energy_budg: <class 'fluidsim.solvers.ns2d.output.spect_energy_budget.SpectralEnergyBudgetNS2D'>
    
    Memory usage at the end of init. (equiv. seq.): 100.00390625 Mo
    Size of state_spect (equiv. seq.): 0.0192 Mo


And then to run the simulation:

.. code:: ipython3

    sim.time_stepping.start()


.. parsed-literal::

    *************************************
    Beginning of the computation
    save state_phys in file state_phys_t000.000_it=0.nc
        compute until t =         10
    it =      0 ; t =          0 ; deltat  =   0.083333
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
    it =      6 ; t =    1.08333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =     0.959 s
    it =     12 ; t =    2.28333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =     0.844 s
    it =     17 ; t =    3.28333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =     0.761 s
    it =     22 ; t =    4.28333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =     0.578 s
    it =     27 ; t =    5.28333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =     0.476 s
    it =     32 ; t =    6.28333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =     0.467 s
    it =     37 ; t =    7.28333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =     0.352 s
    it =     43 ; t =    8.48333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =     0.187 s
    it =     49 ; t =    9.68333 ; deltat  =        0.2
                  energy = 0.000e+00 ; Delta energy = +0.000e+00
                  estimated remaining duration =    0.0371 s
    Computation completed in  1.47815 s
    path_run =
    /home/pierre/Sim_data/NS2D_48x48_S8x8_2018-03-14_07-58-29
    save state_phys in file state_phys_t010.083_it=51.nc


In the following, we are going to understand these 4 lines of code… But
first let’s clean-up by deleting the result directory of this tiny
example simulation:

.. code:: ipython3

    import shutil
    shutil.rmtree(sim.output.path_run)

Importing a solver
------------------

The first line imports a "Simulation" class from a "solver" module. Any solver module has to provide a class called "Simul". We have already seen that the Simul class can be imported like this:

.. code:: ipython3

    from fluidsim.solvers.ns2d.solver import Simul

but there is another convenient way to import it from a string:

.. code:: ipython3

    Simul = fluidsim.import_simul_class_from_key('ns2d')

Create an instance of the class Parameters
------------------------------------------

The next step is to create an object ``params`` from the information
contained in the class ``Simul``:

.. code:: ipython3

    params = Simul.create_default_params()

The object ``params`` is an instance of the class :class:`fluidsim.base.params.Parameters` (which inherits from `fluiddyn.util.paramcontainer.ParamContainer <http://fluiddyn.readthedocs.org/en/latest/generated/fluiddyn.util.paramcontainer.html>`_). It is usually a quite complex hierarchical object containing many attributes.  To print them, the normal way would be to use the tab-completion of Ipython, i.e. to type "`params.`" and press on the tab key. Here with Jupyter, I can not do that so I'm going to use a command that produce a list with the interesting attributes. If you don't understand this command, you should have a look at the section on `list comprehensions <https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions>`_ of the official Python tutorial):

.. code:: ipython3

    [attr for attr in dir(params) if not attr.startswith('_')]




.. parsed-literal::

    ['NEW_DIR_RESULTS',
     'ONLY_COARSE_OPER',
     'beta',
     'forcing',
     'init_fields',
     'nu_2',
     'nu_4',
     'nu_8',
     'nu_m4',
     'oper',
     'output',
     'preprocess',
     'short_name_type_run',
     'time_stepping']



and some useful functions (whose names all start with ``_`` in order to be hidden in Ipython and not mixed with the meaningful parameters): 

.. code:: ipython3

    [attr for attr in dir(params) if attr.startswith('_') and not attr.startswith('__')]




.. parsed-literal::

    ['_contains_doc',
     '_doc',
     '_get_formatted_doc',
     '_get_formatted_docs',
     '_get_key_attribs',
     '_key_attribs',
     '_load_from_elemxml',
     '_load_from_hdf5_file',
     '_load_from_hdf5_object',
     '_load_from_xml_file',
     '_make_dict',
     '_make_dict_attribs',
     '_make_element_xml',
     '_make_full_tag',
     '_make_xml_text',
     '_modif_from_other_params',
     '_parent',
     '_print_as_xml',
     '_print_doc',
     '_print_docs',
     '_save_as_hdf5',
     '_save_as_xml',
     '_set_as_child',
     '_set_attrib',
     '_set_attribs',
     '_set_child',
     '_set_doc',
     '_set_internal_attr',
     '_tag',
     '_tag_children']



Some of the attributes of ``params`` are simple Python objects and others can be other :class:`fluidsim.base.params.Parameters`:

.. code:: ipython3

    print(type(params.nu_2))
    print(type(params.output))


.. parsed-literal::

    <class 'float'>
    <class 'fluidsim.base.params.Parameters'>


.. code:: ipython3

    [attr for attr in dir(params.output) if not attr.startswith('_')]




.. parsed-literal::

    ['HAS_TO_SAVE',
     'ONLINE_PLOT_OK',
     'increments',
     'period_refresh_plots',
     'periods_plot',
     'periods_print',
     'periods_save',
     'phys_fields',
     'spatial_means',
     'spect_energy_budg',
     'spectra',
     'sub_directory']



We see that the object ``params`` contains a tree of parameters. This
tree can be represented as xml code:

.. code:: ipython3

    print(params)


.. parsed-literal::

    <fluidsim.base.params.Parameters object at 0x7f1434b62208>
    
    <params NEW_DIR_RESULTS="True" ONLY_COARSE_OPER="False" beta="0.0" nu_2="0.0"
            nu_4="0.0" nu_8="0.0" nu_m4="0.0" short_name_type_run="">
      <oper Lx="8" Ly="8" coef_dealiasing="0.6666666666666666" nx="48" ny="48"
            type_fft="fft2d.with_pyfftw"/>  
    
      <time_stepping USE_CFL="True" USE_T_END="True" deltat0="0.2" it_end="10"
                     t_end="10.0" type_time_scheme="RK4"/>  
    
      <init_fields available_types="['from_file', 'from_simul', 'in_script',
                   'constant', 'noise', 'jet', 'dipole']" type="constant">
        <from_file path=""/>  
    
        <constant value="1.0"/>  
    
        <noise length="0" velo_max="1.0"/>  
    
      </init_fields>
    
      <forcing available_types="['in_script', 'proportional', 'tcrandom',
               'tcrandom_anisotropic']" enable="False" forcing_rate="1.0"
               key_forced="None" nkmax_forcing="5" nkmin_forcing="4" type="">
        <tcrandom time_correlation="based_on_forcing_rate"
                  type_normalize="2nd_degree_eq"/>  
    
        <tcrandom_anisotropic angle="45" time_correlation="based_on_forcing_rate"
                              type_normalize="2nd_degree_eq"/>  
    
      </forcing>
    
      <output HAS_TO_SAVE="True" ONLINE_PLOT_OK="True" period_refresh_plots="1"
              sub_directory="">
        <periods_save increments="0" phys_fields="0" spatial_means="0"
                      spect_energy_budg="0" spectra="0"/>  
    
        <periods_print print_stdout="1.0"/>  
    
        <periods_plot phys_fields="0"/>  
    
        <phys_fields field_to_plot="rot" file_with_it="False"/>  
    
        <spectra HAS_TO_PLOT_SAVED="False"/>  
    
        <spatial_means HAS_TO_PLOT_SAVED="False"/>  
    
        <spect_energy_budg HAS_TO_PLOT_SAVED="False"/>  
    
        <increments HAS_TO_PLOT_SAVED="False"/>  
    
      </output>
    
      <preprocess enable="False" forcing_const="1.0" forcing_scale="unity"
                  init_field_const="1.0" init_field_scale="unity"
                  viscosity_const="1.0" viscosity_scale="enstrophy_forcing"
                  viscosity_type="laplacian"/>  
    
    </params>
    


Set the parameters for your simulation
--------------------------------------

The user can change any parameters

.. code:: ipython3

    params.nu_2 = 1e-3
    params.forcing.enable = False
    
    params.init_fields.type = 'noise'
    
    params.output.periods_save.spatial_means = 1.
    params.output.periods_save.spectra = 1.
    params.output.periods_save.phys_fields = 2.

but it is impossible to create accidentally a parameter which is actually not used:

.. code:: ipython3

    try:
        params.this_param_does_not_exit = 10
    except AttributeError as e:
        print('AttributeError:', e)


.. parsed-literal::

    AttributeError: this_param_does_not_exit is not already set in params.
    The attributes are: ['NEW_DIR_RESULTS', 'ONLY_COARSE_OPER', 'beta', 'nu_2', 'nu_4', 'nu_8', 'nu_m4', 'short_name_type_run']
    To set a new attribute, use _set_attrib or _set_attribs.


And you also get an explicit error message if you use a nonexistent
parameter:

.. code:: ipython3

    try:
        print(params.this_param_does_not_exit)
    except AttributeError as e:
        print('AttributeError:', e)


.. parsed-literal::

    AttributeError: this_param_does_not_exit is not an attribute of params.
    The attributes are: ['NEW_DIR_RESULTS', 'ONLY_COARSE_OPER', 'beta', 'nu_2', 'nu_4', 'nu_8', 'nu_m4', 'short_name_type_run']
    The children are: ['oper', 'time_stepping', 'init_fields', 'forcing', 'output', 'preprocess']


This behaviour is much safer than using a text file or a python file for
the parameters. In order to discover the different parameters for a
solver, create the ``params`` object containing the default parameters
in Ipython (``params = Simul.create_default_params()``), print it and
use the auto-completion (for example writting ``params.`` and pressing
on the tab key).

Instantiate a simulation object
-------------------------------

The next step is to create a simulation object (an instance of the class
``solver.Simul``) with the parameters in ``params``:

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
    /home/pierre/Sim_data/NS2D_48x48_S8x8_2018-03-14_07-58-33
    init_fields.type: noise
    
    Initialization outputs:
    sim.output.phys_fields:       <class 'fluidsim.base.output.phys_fields.PhysFieldsBase2D'>
    sim.output.spectra:           <class 'fluidsim.solvers.ns2d.output.spectra.SpectraNS2D'>
    sim.output.increments:        <class 'fluidsim.base.output.increments.Increments'>
    sim.output.spatial_means:     <class 'fluidsim.solvers.ns2d.output.spatial_means.SpatialMeansNS2D'>
    sim.output.spect_energy_budg: <class 'fluidsim.solvers.ns2d.output.spect_energy_budget.SpectralEnergyBudgetNS2D'>
    
    Memory usage at the end of init. (equiv. seq.): 103.484375 Mo
    Size of state_spect (equiv. seq.): 0.0192 Mo


which initializes everything needed to run the simulation.

The log shows the object-oriented structure of the solver. Every task is
performed by an object of a particular class. Of course, you don’t need
to understand the structure of the solver to run simulations but soon
it’s going to be useful to understand what you do and how to interact
with fluidsim objects.

The object ``sim`` has a limited number of attributes:

.. code:: ipython3

    [attr for attr in dir(sim) if not attr.startswith('_')]




.. parsed-literal::

    ['InfoSolver',
     'compute_freq_diss',
     'create_default_params',
     'info',
     'info_solver',
     'init_fields',
     'is_forcing_enabled',
     'name_run',
     'oper',
     'output',
     'params',
     'preprocess',
     'state',
     'tendencies_nonlin',
     'time_stepping']



In the tutorial `Understand how FluidSim works <tuto_dev.html>`_, we will see what are all these attributes.

The object ``sim.info`` is a :class:`fluiddyn.util.paramcontainer.ParamContainer` which contains all the information on the solver (in ``sim.info.solver``) and on specific parameters for this simulation (in ``sim.info.solver``):

.. code:: ipython3

    print(sim.info.__class__)
    print([attr for attr in dir(sim.info) if not attr.startswith('_')])


.. parsed-literal::

    <class 'fluiddyn.util.paramcontainer.ParamContainer'>
    ['params', 'solver']


.. code:: ipython3

    sim.info.solver is sim.info_solver




.. parsed-literal::

    True



.. code:: ipython3

    sim.info.params is sim.params




.. parsed-literal::

    True



.. code:: ipython3

    print(sim.info.solver)


.. parsed-literal::

    <fluidsim.solvers.ns2d.solver.InfoSolverNS2D object at 0x7f1434b620f0>
    
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
    


We see that a solver is defined by the classes it uses for some tasks. The tutorial `Understand how FluidSim works <tuto_dev.html>`_ is meant to explain how.

Run the simulation
------------------

We can now start the time stepping. Since
``params.time_stepping.USE_T_END is True``, it should loop until
``sim.time_stepping.t`` is equal or larger than
``params.time_stepping.t_end = 10``.

.. code:: ipython3

    sim.time_stepping.start()


.. parsed-literal::

    *************************************
    Beginning of the computation
    save state_phys in file state_phys_t000.000.nc
        compute until t =         10
    it =      0 ; t =          0 ; deltat  =   0.097144
                  energy = 9.159e-02 ; Delta energy = +0.000e+00
    it =     11 ; t =    1.09077 ; deltat  =    0.10203
                  energy = 9.061e-02 ; Delta energy = -9.864e-04
                  estimated remaining duration =      1.63 s
    save state_phys in file state_phys_t002.025.nc
    it =     21 ; t =    2.12928 ; deltat  =    0.10431
                  energy = 8.968e-02 ; Delta energy = -9.245e-04
                  estimated remaining duration =      2.55 s
    it =     31 ; t =    3.16786 ; deltat  =    0.10207
                  energy = 8.878e-02 ; Delta energy = -9.066e-04
                  estimated remaining duration =      1.48 s
    save state_phys in file state_phys_t004.077.nc
    it =     41 ; t =    4.17641 ; deltat  =   0.097365
                  energy = 8.792e-02 ; Delta energy = -8.570e-04
                  estimated remaining duration =      2.39 s
    it =     52 ; t =    5.25153 ; deltat  =   0.099416
                  energy = 8.704e-02 ; Delta energy = -8.799e-04
                  estimated remaining duration =      1.15 s
    save state_phys in file state_phys_t006.081.nc
    it =     62 ; t =     6.2964 ; deltat  =    0.10757
                  energy = 8.622e-02 ; Delta energy = -8.151e-04
                  estimated remaining duration =      1.59 s
    it =     72 ; t =    7.35201 ; deltat  =    0.10534
                  energy = 8.544e-02 ; Delta energy = -7.822e-04
                  estimated remaining duration =     0.702 s
    save state_phys in file state_phys_t008.113.nc
    it =     82 ; t =    8.43819 ; deltat  =    0.10677
                  energy = 8.468e-02 ; Delta energy = -7.655e-04
                  estimated remaining duration =     0.555 s
    it =     92 ; t =    9.47625 ; deltat  =    0.10177
                  energy = 8.398e-02 ; Delta energy = -6.984e-04
                  estimated remaining duration =     0.132 s
    Computation completed in  3.34398 s
    path_run =
    /home/pierre/Sim_data/NS2D_48x48_S8x8_2018-03-14_07-58-33
    save state_phys in file state_phys_t010.087.nc


Analyze the output
------------------

Let’s see what we can do with the object ``sim.output``. What are its
attributes?

.. code:: ipython3

    [attr for attr in dir(sim.output) if not attr.startswith('_')]




.. parsed-literal::

    ['compute_energy',
     'compute_energy_fft',
     'compute_enstrophy',
     'compute_enstrophy_fft',
     'end_of_simul',
     'figure_axe',
     'increments',
     'init_with_initialized_state',
     'init_with_oper_and_state',
     'name_run',
     'name_solver',
     'one_time_step',
     'oper',
     'params',
     'path_run',
     'phys_fields',
     'print_size_in_Mo',
     'print_stdout',
     'sim',
     'spatial_means',
     'spect_energy_budg',
     'spectra',
     'sum_wavenumbers']



Many of these objects (``print_stdout``, ``phys_fields``,
``spatial_means``, ``spect_energy_budg``, ``spectra``, …) were used
during the simulation to save outputs. They can also load the data and
produce some simple plots.

Let’s say that it is very simple to reload an old simulation from the
saved files. There are two convenient functions to do this
``fluidsim.load_sim_for_plot`` and ``fluidsim.load_state_phys_file``:

.. code:: ipython3

    from fluidsim import load_sim_for_plot

.. code:: ipython3

    print(load_sim_for_plot.__doc__)


.. parsed-literal::

    Create a object Simul from a dir result.
    
        Creating simulation objects with this function should be fast because the
        state is not initialized with the output file and only a coarse operator is
        created.
    
        Parameters
        ----------
    
        path_dir : str (optional)
    
          Path of the directory of the simulation.
    
        merge_missing_params : bool (optional, default == False)
    
          Can be used to load old simulations carried out with an old fluidsim
          version.
    
        


.. code:: ipython3

    from fluidsim import load_state_phys_file

.. code:: ipython3

    print(load_state_phys_file.__doc__)


.. parsed-literal::

    Create a simulation from a file.
    
        For large resolution, creating a simulation object with this function can
        be slow because the state is initialized with the output file.
    
        Parameters
        ----------
    
        name_dir : str (optional)
    
          Name of the directory of the simulation. If nothing is given, we load the
          data in the current directory.
    
        t_approx : number (optional)
    
          Approximate time of the file to be loaded.
    
        modif_save_params :  bool (optional, default == True)
    
          If True, the parameters of the simulation are modified before loading::
    
            params.output.HAS_TO_SAVE = False
            params.output.ONLINE_PLOT_OK = False
    
        merge_missing_params : bool (optional, default == False)
    
          Can be used to load old simulations carried out with an old fluidsim
          version.
    
        


.. code:: ipython3

    sim = load_state_phys_file(sim.output.path_run)


.. parsed-literal::

    *************************************
    Program fluidsim
    Load state from file:
    [...]/pierre/Sim_data/NS2D_48x48_S8x8_2018-03-14_07-58-33/state_phys_t010.087.nc
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
    /home/pierre/Sim_data/NS2D_48x48_S8x8_2018-03-14_07-58-33
    init_fields.type: from_file
    
    Initialization outputs:
    sim.output.phys_fields:       <class 'fluidsim.base.output.phys_fields.PhysFieldsBase2D'>
    sim.output.spectra:           <class 'fluidsim.solvers.ns2d.output.spectra.SpectraNS2D'>
    sim.output.increments:        <class 'fluidsim.base.output.increments.Increments'>
    sim.output.spatial_means:     <class 'fluidsim.solvers.ns2d.output.spatial_means.SpatialMeansNS2D'>
    sim.output.spect_energy_budg: <class 'fluidsim.solvers.ns2d.output.spect_energy_budget.SpectralEnergyBudgetNS2D'>
    
    Memory usage at the end of init. (equiv. seq.): 104.21484375 Mo
    Size of state_spect (equiv. seq.): 0.0192 Mo


For example, to display the time evolution of spatially averaged
quantities (here the energy, the entrophy and their dissipation rate):

.. code:: ipython3

     sim.output.spatial_means.plot()



.. image:: tuto_user_files/tuto_user_61_0.png



.. image:: tuto_user_files/tuto_user_61_1.png


To plot the final state:

.. code:: ipython3

    sim.output.phys_fields.plot()



.. image:: tuto_user_files/tuto_user_63_0.png


And a different time:

.. code:: ipython3

    sim.output.phys_fields.plot(time=4)



.. image:: tuto_user_files/tuto_user_65_0.png


We can even plot variables that are not in the state in the solver. For
example, in this solver, the divergence, which should be equal to 0:

.. code:: ipython3

    sim.output.phys_fields.plot('div')



.. image:: tuto_user_files/tuto_user_67_0.png


Finally we remove the directory of this example simulation…

.. code:: ipython3

    shutil.rmtree(sim.output.path_run)
