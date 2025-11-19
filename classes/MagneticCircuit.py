import numpy as np
from classes.MagneticParameters import *

class MagneticCircuit:

    def __init__(self, gap_magnetic_flux_density, bore_radius, n_pole, lz_machine, b_of_h, n_stator_slot, n_rotor_slot, stator_yoke_thickness, rotor_yoke_thickness, stator_slot_length, rotor_slot_length):
        self._gap_magnetic_flux_density = gap_magnetic_flux_density
        self._bore_radius = bore_radius
        self._n_pole = n_pole
        self._lz_machine = lz_machine
        self._b_of_h = b_of_h
        self._n_stator_slot = n_stator_slot
        self._n_rotor_slot = n_rotor_slot
        self._stator_yoke_thickness = stator_yoke_thickness
        self._rotor_yoke_thickness = rotor_yoke_thickness
        self._stator_slot_length = stator_slot_length
        self._rotor_slot_length = rotor_slot_length

    def __get_surface(self, length, n_slot):
        return length * self._lz_machine*n_slot/self._n_pole

    @property
    def get_stator_yoke_magnetic_surface(self):
        return self.__get_surface(self._stator_yoke_thickness, self._n_stator_slot)

    @property
    def get_rotor_yoke_magnetic_surface(self):
        return self.__get_surface(self._rotor_yoke_thickness, self._n_rotor_slot)

    @property
    def get_stator_teeth_magnetic_surface(self):
        return self.__get_surface(self._stator_slot_length, self._n_stator_slot)

    @property
    def get_rotor_teeth_magnetic_surface(self):
        return self.__get_surface(self._rotor_slot_length, self._n_rotor_slot)

    @property
    def get_pole_magnetic_surface(self):
        return self._bore_radius*2*np.pi/self._n_pole*self._lz_machine

    @property
    def get_stator_yoke_magnetic_flux_density(self):
        return MagneticParametersFromMagneticFluxDensity(self._gap_magnetic_flux_density * self.get_pole_magnetic_surface * self._n_pole / self._n_stator_slot / self.get_stator_yoke_magnetic_surface, self._b_of_h)

    @property
    def get_rotor_yoke_magnetic_flux_density(self):
        return MagneticParametersFromMagneticFluxDensity(self._gap_magnetic_flux_density * self.get_pole_magnetic_surface * self._n_pole / self._n_rotor_slot / self.get_rotor_yoke_magnetic_surface, self._b_of_h)

    @property
    def get_stator_teeth_magnetic_flux_density(self):
        return MagneticParametersFromMagneticFluxDensity(self._gap_magnetic_flux_density * self.get_pole_magnetic_surface / 2 / self.get_stator_teeth_magnetic_surface, self._b_of_h)

    @property
    def get_rotor_teeth_magnetic_flux_density(self):
        return MagneticParametersFromMagneticFluxDensity(self._gap_magnetic_flux_density * self.get_pole_magnetic_surface / 2 / self.get_rotor_teeth_magnetic_surface, self._b_of_h)

    @property
    def get_pole_magnetic_flux(self):
        return self.get_stator_teeth_magnetic_surface*self.get_stator_teeth_magnetic_flux_density.get_magnetic_flux_density