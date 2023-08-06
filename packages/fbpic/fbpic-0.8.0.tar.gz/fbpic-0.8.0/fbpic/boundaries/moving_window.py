# Copyright 2016, FBPIC contributors
# Authors: Remi Lehe, Manuel Kirchen
# License: 3-Clause-BSD-LBNL
"""
This file is part of the Fourier-Bessel Particle-In-Cell code (FB-PIC)
It defines the structure necessary to implement the moving window.
"""
import numpy as np
from scipy.constants import c
from fbpic.particles import Particles
from fbpic.lpa_utils.boosted_frame import BoostConverter
from fbpic.utils.threading import njit_parallel, prange
# Check if CUDA is available, then import CUDA functions
from fbpic.utils.cuda import cuda_installed
if cuda_installed:
    from fbpic.utils.cuda import cuda, cuda_tpb_bpg_2d

class MovingWindow(object):
    """
    Class that contains the moving window's variables and methods
    """
    def __init__( self, interp, comm, dt, ptcl, v, p_nz, time,
                  ux_m=0., uy_m=0., uz_m=0., ux_th=0., uy_th=0., uz_th=0.,
                  gamma_boost=None ) :
        """
        Initializes a moving window object.

        Parameters
        ----------
        interp: a list of Interpolation objects
            Contains the positions of the boundaries

        comm: a BoundaryCommunicator object
            Contains information about the MPI decomposition
            and about the longitudinal boundaries

        dt: float
            The timestep of the simulation.

        ptcl: a list of Particle objects
            Needed in order to infer the position of injection
            of the particles by the moving window.

        v: float (meters per seconds), optional
            The speed of the moving window

        p_nz: int
            Number of macroparticles per cell along the z direction

        time: float (seconds)
            The time (in the simulation) at which the moving
            window was initialized

        ux_m, uy_m, uz_m: floats (dimensionless)
           Normalized mean momenta of the injected particles in each direction

        ux_th, uy_th, uz_th: floats (dimensionless)
           Normalized thermal momenta in each direction

        gamma_boost : float, optional
            When initializing the laser in a boosted frame, set the
            value of `gamma_boost` to the corresponding Lorentz factor.
            (uz_m is to be given in the lab frame ; for the moment, this
            will not work if any of ux_th, uy_th, uz_th, ux_m, uy_m is nonzero)
        """
        # Check that the boundaries are open
        if ((comm.rank == comm.size-1) and (comm.right_proc is not None)) \
          or ((comm.rank == 0) and (comm.left_proc is not None)):
          raise ValueError('The simulation is using a moving window, but '
                    'the boundaries are periodic.\n Please select open '
                    'boundaries when initializing the Simulation object.')

        # Momenta parameters
        self.ux_m = ux_m
        self.uy_m = uy_m
        self.uz_m = uz_m
        self.ux_th = ux_th
        self.uy_th = uy_th
        self.uz_th = uz_th

        # When running the simulation in boosted frame, convert the arguments
        if gamma_boost is not None:
            boost = BoostConverter( gamma_boost )
            self.uz_m, = boost.longitudinal_momentum([ self.uz_m ])

        # Attach moving window speed and period
        self.v = v

        # Get the positions of the global physical domain
        zmin_global_domain, zmax_global_domain = comm.get_zmin_zmax(
                            local=False, with_damp=False, with_guard=False )

        # Attach reference position of moving window (only for the first proc)
        # (Determines by how many cells the window should be moved)
        if comm.rank == 0:
            self.zmin = zmin_global_domain

        # Attach injection position and speed (only for the last proc)
        if comm.rank == comm.size-1:
            self.v_end_plasma = \
                c * self.uz_m / np.sqrt(1 + ux_m**2 + uy_m**2 + self.uz_m**2)
            # Initialize plasma *ahead* of the right *physical* boundary of
            # the box so, after `exchange_period` iterations
            # (without adding new plasma), there will still be plasma
            # inside the physical domain. ( +3 takes into account that 3 more
            # cells need to be filled w.r.t the left edge of the physical box
            # such that the last cell inside the box is always correct for
            # 1st and 3rd order shape factor particles after the moving window
            # shifted by exchange_period cells. )
            self.z_inject = zmax_global_domain + 3*comm.dz + \
                comm.exchange_period * (v-self.v_end_plasma) * dt
            # Try to detect the position of the end of the plasma:
            # Find the maximal position of the particles which are
            # continously injected.
            self.z_end_plasma = None
            for species in ptcl:
                if species.continuous_injection and species.Ntot != 0:
                    # Add half of the spacing between particles (the injection
                    # function itself will add a half-spacing again)
                    self.z_end_plasma = species.z.max() + 0.5*comm.dz/p_nz
                    break
            # Default value in the absence of continuously-injected particles
            if self.z_end_plasma is None:
                self.z_end_plasma = zmax_global_domain
            self.nz_inject = 0
            self.p_nz = p_nz

        # Attach time of last move
        self.t_last_move = time - dt

    def move_grids(self, fld, comm, time):
        """
        Calculate by how many cells the moving window should be moved.
        If this is non-zero, shift the fields on the interpolation grid,
        and add new particles.

        NB: the spectral grid is not modified, as it is automatically
        updated after damping the fields (see main.py)

        Parameters
        ----------
        fld: a Fields object
            Contains the fields data of the simulation

        comm: an fbpic BoundaryCommunicator object
            Contains the information on the MPI decomposition

        time: float (seconds)
            The global time in the simulation
            This is used in order to determine how much the window should move
        """
        # To avoid discrepancies between processors, only the first proc
        # decides whether to send the data, and broadcasts the information.
        dz = comm.dz
        if comm.rank==0:
            # Move the continuous position of the moving window object
            self.zmin += self.v * (time - self.t_last_move)
            # Find the number of cells by which the window should move
            zmin_global_domain, zmax_global_domain = comm.get_zmin_zmax(
                            local=False, with_damp=False, with_guard=False )
            n_move = int( (self.zmin - zmin_global_domain)/dz )
        else:
            n_move = None
        # Broadcast the information to all proc
        if comm.size > 1:
            n_move = comm.mpi_comm.bcast( n_move )

        # Move the grids
        if n_move != 0:
            # Move the global domain
            comm.shift_global_domain_positions( n_move*dz )
            # Shift the fields
            Nm = len(fld.interp)
            for m in range(Nm):
                # Modify the values of the corresponding z's
                fld.interp[m].zmin += n_move*fld.interp[m].dz
                fld.interp[m].zmax += n_move*fld.interp[m].dz
                # Shift/move fields by n_move cells in spectral space
                self.shift_spect_grid( fld.spect[m], n_move )

        # Because the grids have just been shifted, there is a shift
        # in the cell indices that are used for the prefix sum.
        if fld.use_cuda:
            fld.prefix_sum_shift += n_move
            # This quantity is reset to 0 whenever prefix_sum is recalculated

        # Prepare the positions of injection for the particles
        # (The actual creation of particles is done when the routine
        # exchange_particles of boundary_communicator.py is called)
        if comm.rank == comm.size-1:
            # Move the injection position
            self.z_inject += self.v * (time - self.t_last_move)
            # Take into account the motion of the end of the plasma
            self.z_end_plasma += self.v_end_plasma * (time - self.t_last_move)
            # Increment the number of particle cells to add
            nz_new = int( (self.z_inject - self.z_end_plasma)/dz )
            self.nz_inject += nz_new
            # Increment the virtual position of the end of the plasma
            # (When `generate_particles` is called, then the plasma
            # is injected between z_end_plasma - nz_inject*dz and z_end_plasma,
            # and afterwards nz_inject is set to 0.)
            self.z_end_plasma += nz_new*dz

        # Change the time of the last move
        self.t_last_move = time

    def generate_particles( self, species, dz, time ) :
        """
        Generate new particles at the right end of the plasma
        (i.e. between z_end_plasma - nz_inject*dz and z_end_plasma)

        Return them in the form of a particle buffer of shape (8, Nptcl)

        Parameters
        ----------
        species: a Particles object
            Contains data about the existing particles

        dz: float (meters)
            The grid spacing along see on the grid

        time: float (seconds)
            The global time of the simulation
            (Needed in order to infer how much the plasma has moved)

        Returns
        -------
        - float_buffer: An array of floats of shape (n_float, Nptcl)
            that contain the float properties of the particles
        - uint_buffer: An array of uints of shape (n_int, Nptcl)
            that contain the integer properties of the particles (e.g. id)
        """
        # Shortcut for the number of integer quantities
        n_int = species.n_integer_quantities
        n_float = species.n_float_quantities

        # Create new particle cells
        if (self.nz_inject > 0) and (species.continuous_injection == True):
            # Create a temporary density function that takes into
            # account the fact that the plasma has moved
            if species.dens_func is not None:
                def dens_func( z, r ):
                    return( species.dens_func( z-self.v_end_plasma*time, r ) )
            else:
                dens_func = None
            # Create the particles that will be added
            zmax = self.z_end_plasma
            zmin = self.z_end_plasma - self.nz_inject*dz
            Npz = self.nz_inject * self.p_nz
            new_ptcl = Particles( species.q, species.m, species.n,
                Npz, zmin, zmax, species.Npr, species.rmin, species.rmax,
                species.Nptheta, species.dt, dens_func=dens_func,
                ux_m=self.ux_m, uy_m=self.uy_m, uz_m=self.uz_m,
                ux_th=self.ux_th, uy_th=self.uy_th, uz_th=self.uz_th)

            # Initialize ionization-relevant arrays if species is ionizable
            if species.ionizer is not None:
                new_ptcl.make_ionizable( element=species.ionizer.element,
                    target_species=species.ionizer.target_species,
                    level_start=species.ionizer.level_start,
                    full_initialization=False )
            # Convert them to a particle buffer
            # - Float buffer
            float_buffer = np.empty( (n_float, new_ptcl.Ntot), dtype=np.float64 )
            float_buffer[0,:] = new_ptcl.x
            float_buffer[1,:] = new_ptcl.y
            float_buffer[2,:] = new_ptcl.z
            float_buffer[3,:] = new_ptcl.ux
            float_buffer[4,:] = new_ptcl.uy
            float_buffer[5,:] = new_ptcl.uz
            float_buffer[6,:] = new_ptcl.inv_gamma
            float_buffer[7,:] = new_ptcl.w
            if species.ionizer is not None:
                float_buffer[8,:] = new_ptcl.ionizer.w_times_level
            # - Integer buffer
            uint_buffer = np.empty( (n_int, new_ptcl.Ntot), dtype=np.uint64 )
            i_int = 0
            if species.tracker is not None:
                uint_buffer[i_int,:] = \
                    species.tracker.generate_new_ids(new_ptcl.Ntot)
                i_int += 1
            if species.ionizer is not None:
                uint_buffer[i_int,:] = new_ptcl.ionizer.ionization_level
        else:
            # No new particles: initialize empty arrays
            float_buffer = np.empty( (n_float, 0), dtype=np.float64 )
            uint_buffer = np.empty( (n_int, 0), dtype=np.uint64 )

        return( float_buffer, uint_buffer )

    def shift_spect_grid( self, grid, n_move,
                          shift_rho=True, shift_currents=True ):
        """
        Shift the spectral fields by n_move cells (with respect to the
        spatial grid). Shifting is done either on the CPU or the GPU,
        if use_cuda is True. (Typically n_move is positive, and the
        fields are shifted backwards)

        Parameters
        ----------
        grid: an SpectralGrid corresponding to one given azimuthal mode
            Contains the values of the fields in spectral space,
            and is modified by this function.

        n_move: int
            The number of cells by which the grid should be shifted

        shift_rho: bool, optional
            Whether to also shift the charge density
            Default: True, since rho is only recalculated from
            scratch when the particles are exchanged

        shift_currents: bool, optional
            Whether to also shift the currents
            Default: False, since the currents are recalculated from
            scratch at each PIC cycle
        """
        if grid.use_cuda:
            shift = grid.d_field_shift
            # Get a 2D CUDA grid of the size of the grid
            tpb, bpg = cuda_tpb_bpg_2d( grid.Ep.shape[0], grid.Ep.shape[1] )
            # Shift all the fields on the GPU
            shift_spect_array_gpu[tpb, bpg]( grid.Ep, shift, n_move )
            shift_spect_array_gpu[tpb, bpg]( grid.Em, shift, n_move )
            shift_spect_array_gpu[tpb, bpg]( grid.Ez, shift, n_move )
            shift_spect_array_gpu[tpb, bpg]( grid.Bp, shift, n_move )
            shift_spect_array_gpu[tpb, bpg]( grid.Bm, shift, n_move )
            shift_spect_array_gpu[tpb, bpg]( grid.Bz, shift, n_move )
            if shift_rho:
                shift_spect_array_gpu[tpb, bpg]( grid.rho_prev, shift, n_move )
            if shift_currents:
                shift_spect_array_gpu[tpb, bpg]( grid.Jp, shift, n_move )
                shift_spect_array_gpu[tpb, bpg]( grid.Jm, shift, n_move )
                shift_spect_array_gpu[tpb, bpg]( grid.Jz, shift, n_move )
        else:
            shift = grid.field_shift
            # Shift all the fields on the CPU
            shift_spect_array_cpu( grid.Ep, shift, n_move )
            shift_spect_array_cpu( grid.Em, shift, n_move )
            shift_spect_array_cpu( grid.Ez, shift, n_move )
            shift_spect_array_cpu( grid.Bp, shift, n_move )
            shift_spect_array_cpu( grid.Bm, shift, n_move )
            shift_spect_array_cpu( grid.Bz, shift, n_move )
            if shift_rho:
                shift_spect_array_cpu( grid.rho_prev, shift, n_move )
            if shift_currents:
                shift_spect_array_cpu( grid.Jp, shift, n_move )
                shift_spect_array_cpu( grid.Jm, shift, n_move )
                shift_spect_array_cpu( grid.Jz, shift, n_move )

@njit_parallel
def shift_spect_array_cpu( field_array, shift_factor, n_move ):
    """
    Shift the field 'field_array' by n_move cells on CPU.
    This is done in spectral space and corresponds to multiplying the
    fields with the factor exp(i*kz_true*dz)**n_move .

    Parameters
    ----------
    field_array: 2darray of complexs
        Contains the value of the fields, and is modified by
        this function

    shift_factor: 1darray of complexs
        Contains the shift array, that is multiplied to the fields in
        spectral space to shift them by one cell in spatial space
        ( exp(i*kz_true*dz) )

    n_move: int
        The number of cells by which the grid should be shifted
    """
    Nz, Nr = field_array.shape

    # Loop over the 2D array (in parallel over z if threading is enabled)
    for iz in prange( Nz ):
        power_shift = 1. + 0.j
        # Calculate the shift factor (raising to the power n_move ;
        # for negative n_move, we take the complex conjugate, since
        # shift_factor is of the form e^{i k dz})
        for i in range( abs(n_move) ):
            power_shift *= shift_factor[iz]
        if n_move < 0:
            power_shift = power_shift.conjugate()
        # Shift the fields
        for ir in range( Nr ):
            field_array[iz, ir] *= power_shift

if cuda_installed:

    @cuda.jit
    def shift_spect_array_gpu( field_array, shift_factor, n_move ):
        """
        Shift the field 'field_array' by n_move cells on the GPU.
        This is done in spectral space and corresponds to multiplying the
        fields with the factor exp(i*kz_true*dz)**n_move .

        Parameters
        ----------
        field_array: 2darray of complexs
            Contains the value of the fields, and is modified by
            this function

        shift_factor: 1darray of complexs
            Contains the shift array, that is multiplied to the fields in
            spectral space to shift them by one cell in spatial space
            ( exp(i*kz_true*dz) )

        n_move: int
            The number of cells by which the grid should be shifted
        """
        # Get a 2D CUDA grid
        iz, ir = cuda.grid(2)

        # Only access values that are actually in the array
        if ir < field_array.shape[1] and iz < field_array.shape[0]:
            power_shift = 1. + 0.j
            # Calculate the shift factor (raising to the power n_move ;
            # for negative n_move, we take the complex conjugate, since
            # shift_factor is of the form e^{i k dz})
            for i in range( abs(n_move) ):
                power_shift *= shift_factor[iz]
            if n_move < 0:
                power_shift = power_shift.conjugate()
            # Shift fields
            field_array[iz, ir] *= power_shift
