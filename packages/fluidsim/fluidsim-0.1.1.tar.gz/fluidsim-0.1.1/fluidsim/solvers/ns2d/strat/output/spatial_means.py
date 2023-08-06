"""Spatial means (:mod:`fluidsim.solvers.ns2d.strat.output.spatial_means`)
==========================================================================

.. autoclass:: SpatialMeansNS2DStrat
   :members:
   :private-members:

"""

from __future__ import division, print_function

import os
import numpy as np


from fluiddyn.util import mpi

from fluidsim.base.output.spatial_means import SpatialMeansBase


class SpatialMeansNS2DStrat(SpatialMeansBase):
    """Spatial means output stratified fluid"""

    def _save_one_time(self):
        tsim = self.sim.time_stepping.t
        self.t_last_save = tsim

        # Compute the kinetic, potential energy and enstrophy
        energyK_fft, energyA_fft = self.output.compute_energies_fft()
        enstrophy_fft = self.output.compute_enstrophy_fft()
        enstrophy = self.sum_wavenumbers(enstrophy_fft)
        energy_fft = self.output.compute_energy_fft()
        energy = self.sum_wavenumbers(energy_fft)

        # Compute energy of the shear modes. (Not implemented in MPI)
        if mpi.nb_proc > 1:
            energy_shear = np.NaN
        else:
            energy_shear = np.sum(energy_fft[:, 0])

        # Dissipation rate kinetic and potential energy (kappa = viscosity)
        f_d, f_d_hypo = self.sim.compute_freq_diss()

        epsK = self.sum_wavenumbers(f_d*2.*energyK_fft)
        epsK_hypo = self.sum_wavenumbers(f_d_hypo*2.*energyK_fft)

        epsA = self.sum_wavenumbers(f_d*2.*energyA_fft)
        epsA_hypo = self.sum_wavenumbers(f_d_hypo*2.*energyA_fft)

        epsZ = self.sum_wavenumbers(f_d*2.*enstrophy_fft)
        epsZ_hypo = self.sum_wavenumbers(f_d_hypo*2.*enstrophy_fft)

        # Injection energy if forcing is True
        if self.sim.params.forcing.enable:
            deltat = self.sim.time_stepping.deltat
            Frot_fft = self.sim.forcing.get_forcing().get_var('rot_fft')
            Fx_fft, Fy_fft = self.vecfft_from_rotfft(Frot_fft)

            rot_fft = self.sim.state.state_spect.get_var('rot_fft')

            ux_fft, uy_fft = self.vecfft_from_rotfft(rot_fft)

            PZ1_fft = np.real(
                rot_fft.conj()*Frot_fft +
                rot_fft*Frot_fft.conj())/2
            PZ2_fft = (abs(Frot_fft)**2)*deltat/2

            PZ1 = self.sum_wavenumbers(PZ1_fft)
            PZ2 = self.sum_wavenumbers(PZ2_fft)


            PK1_fft = np.real(
                ux_fft.conj()*Fx_fft +
                ux_fft*Fx_fft.conj() +
                uy_fft.conj()*Fy_fft +
                uy_fft*Fy_fft.conj())/2
            PK2_fft = (abs(Fx_fft)**2+abs(Fy_fft)**2)*deltat/2

            PK1 = self.sum_wavenumbers(PK1_fft)
            PK2 = self.sum_wavenumbers(PK2_fft)

        if mpi.rank == 0:
            epsK_tot = epsK + epsK_hypo

            self.file.write(
                '####\ntime = {0:7.3f}\n'.format(tsim))
            to_print = (
'E    = {0:11.6e} ; Z         = {1:11.6e} ; E_shear  = {2:11.6e}\n'
'epsA = {3:11.6e} ; epsA_hypo = {4:11.6e} ; epsA_tot = {5:11.9e} \n'
'epsK = {6:11.6e} ; epsK_hypo = {7:11.6e} ; epsK_tot = {8:11.6e} \n'
'epsZ = {9:11.6e} ; epsZ_hypo = {10:11.6e} ; epsZ_tot = {11:11.6e} \n'
).format(energy, enstrophy, energy_shear,
         epsA, epsA_hypo, epsA+epsA_hypo,
         epsK, epsK_hypo, epsK+epsK_hypo,
         epsZ, epsZ_hypo, epsZ+epsZ_hypo)
            self.file.write(to_print)

            if self.sim.params.forcing.enable:
                PK_tot = PK1+PK2
                to_print = (
'PK1  = {0:11.6e} ; PK2       = {1:11.6e} ; PK_tot   = {2:11.6e} \n'
'PZ1  = {3:11.6e} ; PZ2       = {4:11.6e} ; PZ_tot   = {5:11.6e} \n'
).format(PK1, PK2, PK1+PK2, PZ1, PZ2, PZ1+PZ2)
                self.file.write(to_print)

            self.file.flush()
            os.fsync(self.file.fileno())

        if self.has_to_plot and mpi.rank == 0:

            self.axe_a.plot(tsim, energy, 'k.')

            self.axe_b.plot(tsim, epsK_tot, 'k.')
            if self.sim.params.forcing.enable:
                self.axe_b.plot(tsim, PK_tot, 'm.')

            if (tsim-self.t_last_show >= self.period_show):
                self.t_last_show = tsim
                fig = self.axe_a.get_figure()
                fig.canvas.draw()

    def load(self):
        """Generates a dictionary with the output values"""
        dico_results = {'name_solver': self.output.name_solver}

        file_means = open(self.path_file)
        lines = file_means.readlines()

        lines_t = []
        lines_E = []
        lines_PK = []
        lines_PZ = []
        lines_epsK = []
        lines_epsZ = []
        lines_epsA = []

        for il, line in enumerate(lines):
            if line.startswith('time ='):
                lines_t.append(line)
            if line.startswith('E    ='):
                lines_E.append(line)
            if line.startswith('PK1  ='):
                lines_PK.append(line)
            if line.startswith('PZ1  ='):
                lines_PZ.append(line)
            if line.startswith('epsK ='):
                lines_epsK.append(line)
            if line.startswith('epsZ ='):
                lines_epsZ.append(line)
            if line.startswith('epsA ='):
                lines_epsA.append(line)

        nt = len(lines_t)
        if nt > 1:
            nt -= 1

        t = np.empty(nt)
        E = np.empty(nt)
        E_shear = np.empty(nt)
        Z = np.empty(nt)
        PK1 = np.empty(nt)
        PK2 = np.empty(nt)
        PK_tot = np.empty(nt)
        PZ1 = np.empty(nt)
        PZ2 = np.empty(nt)
        PZ_tot = np.empty(nt)
        epsK = np.empty(nt)
        epsK_hypo = np.empty(nt)
        epsK_tot = np.empty(nt)
        epsZ = np.empty(nt)
        epsZ_hypo = np.empty(nt)
        epsZ_tot = np.empty(nt)
        epsA = np.empty(nt)
        epsA_hypo = np.empty(nt)
        epsA_tot = np.empty(nt)

        for il in range(nt):
            line = lines_t[il]
            words = line.split()
            t[il] = float(words[2])

            line = lines_E[il]
            words = line.split()
            E[il] = float(words[2])
            Z[il] = float(words[6])
            E_shear[il] = float(words[10])

            if self.sim.params.forcing.enable:
                line = lines_PK[il]
                words = line.split()
                PK1[il] = float(words[2])
                PK2[il] = float(words[6])
                PK_tot[il] = float(words[10])

                line = lines_PZ[il]
                words = line.split()
                PZ1[il] = float(words[2])
                PZ2[il] = float(words[6])
                PZ_tot[il] = float(words[10])

            line = lines_epsK[il]
            words = line.split()
            epsK[il] = float(words[2])
            epsK_hypo[il] = float(words[6])
            epsK_tot[il] = float(words[10])

            line = lines_epsZ[il]
            words = line.split()
            epsZ[il] = float(words[2])
            epsZ_hypo[il] = float(words[6])
            epsZ_tot[il] = float(words[10])

            line = lines_epsA[il]
            words = line.split()
            epsA[il] = float(words[2])
            epsA_hypo[il] = float(words[6])
            epsA_tot[il] = float(words[10])

        dico_results['t'] = t
        dico_results['E'] = E
        dico_results['Z'] = Z
        dico_results['E_shear'] = E_shear

        dico_results['PK1'] = PK1
        dico_results['PK2'] = PK2
        dico_results['PK_tot'] = PK_tot

        dico_results['PZ1'] = PZ1
        dico_results['PZ2'] = PZ2
        dico_results['PZ_tot'] = PZ_tot

        dico_results['epsK'] = epsK
        dico_results['epsK_hypo'] = epsK_hypo
        dico_results['epsK_tot'] = epsK_tot

        dico_results['epsZ'] = epsZ
        dico_results['epsZ_hypo'] = epsZ_hypo
        dico_results['epsZ_tot'] = epsZ_tot

        dico_results['epsA'] = epsA
        dico_results['epsA_hypo'] = epsA_hypo
        dico_results['epsA_tot'] = epsA_tot

        return dico_results

    def plot(self):
        dico_results = self.load()

        t = dico_results['t']
        E = dico_results['E']
        Z = dico_results['Z']

        epsK = dico_results['epsK']
        epsK_hypo = dico_results['epsK_hypo']
        epsK_tot = dico_results['epsK_tot']

        epsZ = dico_results['epsZ']
        epsZ_hypo = dico_results['epsZ_hypo']
        epsZ_tot = dico_results['epsZ_tot']

        epsA = dico_results['epsA']
        epsA_hypo = dico_results['epsA_hypo']
        epsA_tot = dico_results['epsA_tot']

        width_axe = 0.85
        height_axe = 0.39
        x_left_axe = 0.12
        z_bottom_axe = 0.55

        size_axe = [x_left_axe, z_bottom_axe,
                    width_axe, height_axe]
        fig, ax1 = self.output.figure_axe(size_axe=size_axe)
        fig.suptitle('Energy and enstrophy')
        ax1.set_ylabel('$E(t)$')
        ax1.plot(t, E, 'k', linewidth=2)

        z_bottom_axe = 0.08
        size_axe[1] = z_bottom_axe
        ax2 = fig.add_axes(size_axe)
        ax2.set_ylabel('$Z(t)$')
        ax2.set_xlabel('$t$')
        ax2.plot(t, Z, 'k', linewidth=2)

        z_bottom_axe = 0.54
        size_axe[1] = z_bottom_axe
        fig, ax1 = self.output.figure_axe(size_axe=size_axe)
        fig.suptitle('Dissipation of energy and enstrophy')
        ax1.set_ylabel(r'$\epsilon (t) = \epsilon_K + \epsilon_A$')


        ax1.plot(t, epsK+epsA, 'r', label=r'$\epsilon$', linewidth=2)
        ax1.plot(t, epsK_hypo+epsA_hypo, 'g', label=r'$\epsilon_{hypo}$',
                 linewidth=2)
        ax1.plot(t, epsK_tot+epsA_tot, 'k', label=r'$\epsilon_{tot}$',
                 linewidth=2)

        z_bottom_axe = 0.08
        size_axe[1] = z_bottom_axe
        ax2 = fig.add_axes(size_axe)
        ax2.set_xlabel('$t$')
        ax2.set_ylabel(r'$\epsilon_Z(t)$')

        ax2.plot(t, epsZ, 'r', linewidth=2)
        ax2.plot(t, epsZ_hypo, 'g', linewidth=2)
        ax2.plot(t, epsZ_tot, 'k', linewidth=2)

        if self.sim.params.forcing.enable:
            PK_tot = dico_results['PK_tot']
            PZ_tot = dico_results['PZ_tot']
            ax1.plot(t, PK_tot, 'c', label='P', linewidth=2)
            ax2.plot(t, PZ_tot, 'c', label='P', linewidth=2)
            ax1.set_ylabel('P_E(t), epsK(t)')
            ax2.set_ylabel('P_Z(t), epsZ(t)')

        ax1.legend()
