"""Forcing schemes (:mod:`fluidsim.base.forcing.base`)
============================================================


Provides:

.. autoclass:: ForcingBase
   :members:
   :private-members:

.. autoclass:: ForcingBasePseudoSpectral
   :members:
   :private-members:

"""

from builtins import object

from fluiddyn.util import mpi


class ForcingBase(object):
    """Organize the forcing schemes (base class)"""
    @staticmethod
    def _complete_info_solver(info_solver, classes=None):
        """Complete the ParamContainer info_solver."""
        info_solver.classes.Forcing._set_child('classes')

        if classes is not None:
            classesXML = info_solver.classes.Forcing.classes

            for cls in classes:
                classesXML._set_child(
                    cls.tag,
                    attribs={'module_name': cls.__module__,
                             'class_name': cls.__name__})

    @staticmethod
    def _complete_params_with_default(params, info_solver):
        """This static method is used to complete the *params* container.
        """
        params._set_child(
            'forcing',
            attribs={'enable': False,
                     'type': '',
                     'available_types': [],
                     'forcing_rate': 1.,
                     'key_forced': None})

        params.forcing._set_doc("""

type : str

  Type of forcing.

available_types : list

  Available types that can be used.

forcing_rate : float

  Forcing (energy? depends on the solver) injection rate.

key_forced: {None} or str

  The key of the variable to be forced. If it is None, a default key depending
  of the type of forcing is used.

""")

        dict_classes = info_solver.classes.Forcing.import_classes()
        # iter on the dict in a determined order
        keys = list(dict_classes.keys())
        keys.sort()
        for key in keys:
            cls = dict_classes[key]
            if hasattr(cls, '_complete_params_with_default'):
                cls._complete_params_with_default(params)

    def __init__(self, sim):
        self.type_forcing = sim.params.forcing.type

        dict_classes = sim.info.solver.classes.Forcing.import_classes()

        if self.type_forcing not in dict_classes:

            # temporary trick to open old simulations
            if self.type_forcing == 'random' and 'tcrandom' in dict_classes:
                self.type_forcing = 'tcrandom'
                sim.params.forcing.__dict__['tcrandom'] = \
                    sim.params.forcing['random']
            else:
                if mpi.rank == 0:
                    print('dict_classes:', dict_classes)
                raise ValueError('Wrong value for params.forcing.type: ' +
                                 self.type_forcing)

        ClassForcing = dict_classes[self.type_forcing]

        self.forcing_maker = ClassForcing(sim)

    def __call__(self, key):
        """Return the variable corresponding to the given key."""
        forcing = self.get_forcing()
        return forcing.get_var(key)

    def compute(self):
        self.forcing_maker.compute()

    def get_forcing(self):
        return self.forcing_maker.forcing_phys


class ForcingBasePseudoSpectral(ForcingBase):
    """Organize the forcing schemes (pseudo-spectra)

    .. inheritance-diagram:: ForcingBasePseudoSpectral

    """

    @staticmethod
    def _complete_params_with_default(params, info_solver):
        """This static method is used to complete the *params* container.
        """
        ForcingBase._complete_params_with_default(params, info_solver)

        params.forcing._set_attribs({'nkmax_forcing': 5, 'nkmin_forcing': 4})

    def get_forcing(self):
        return self.forcing_maker.forcing_fft
