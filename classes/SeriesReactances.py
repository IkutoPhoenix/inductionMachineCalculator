import numpy as np
from classes.Winding import *
from classes.Reactance import *
from classes.Coefs import *

class SeriesReactance():

    def __init__(self, n_phases: int, frequency: float, winding: Winding, n_pole: int, slot_width: float, slot_height: float, lz_machine: float, magnetic_reactance: Reactance, air_gap_length: float, voltage_input: float):
        self._n_phases = n_phases
        self._frequency = frequency
        self._winding = winding
        self._n_pole = n_pole
        self._slot_width = slot_width
        self._slot_height = slot_height
        self._lz_machine = lz_machine
        self._magnetic_reactance = magnetic_reactance
        self._air_gap_length = air_gap_length
        self._voltage_input = voltage_input

        self._step_factor = 1
        pass

    @property
    def get_slot_factor(self): # Get slot factor for a rectangular shaped slot
        return self._slot_height/self._slot_width

    @property
    def get_slot_leakage_reactance(self):
        return ReactanceFromValue(8 * (np.pi**2) * (self._winding.get_n_turns**2) * self._n_phases * self._frequency * self._lz_machine*1000 * (self._winding.get_winding_distribution_factor**2) * self.get_slot_factor / (10**10 * self._winding.get_n_slot))

    @property
    def get_differential_leakage_reactance(self):
        return ReactanceFromValue(5/6 * self._magnetic_reactance.get_value*(self._n_pole*2 / self._winding.get_n_slot)**2)

    @property
    def get_slot_flux(self):
        return 0.97*self._voltage_input/(2.22*self._winding.get_n_turns*self._frequency*self._winding.get_winding_distribution_factor)

    @property
    def get_total_flux(self):
        return self._n_pole * self.get_slot_flux/0.637

    @property
    def get_air_gap_flux_density(self):
        return self.get_total_flux*10**6/(np.pi*self._winding.get_bore_radius*self._lz_machine*1000)

    @property
    def get_magnetizing_force(self):
        return 796*self.get_air_gap_flux_density*self._air_gap_length*CarterCoefficient(self._slot_width, self._winding, self._air_gap_length).get_value
    
    @property
    def get_magnetizing_current(self):
        # flux shape factor = 1.11
        # step factor = 1
        return 2*1.11*self.get_magnetizing_force*self._n_pole/(self._n_phases*self._winding.get_n_turns*self._winding.get_winding_distribution_factor*1)

    @property
    def get_loop_leakage_reactance(self):
        # loop leakage factor = 0.0022
        return ReactanceFromValue(self._voltage_input/self.get_magnetizing_current*0.0022)

    @property
    def get_reactance(self):
        return ReactanceFromValue(self.get_differential_leakage_reactance.get_value + self.get_loop_leakage_reactance.get_value + self.get_slot_leakage_reactance.get_value)