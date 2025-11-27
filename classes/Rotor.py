from abc import ABC, abstractmethod
from classes.Winding import *
from classes.Wire import *
from classes.Resistance import *
from classes.COne import *
from classes.Coefs import *


class Rotor(ABC):

    def __init__(self):
        pass

class WoundRotor(Rotor):

    def __init__(self, n_pole: int, n_phase: int, n_rotor_slot: int, voltage_input: float, frequency: float, rotor_radius: float, lz_machine: float, n_rotor_turns: int, rotor_power: float, rotor_wire: Wire, stator_winding: Winding):
        super().__init__()
        self._n_rotor_conductors = 1
        self._stator_step_factor = 1
        self._rotor_winding_distribution_factor = 1
        self._rotor_step_factor = 1
        self._n_bar = 1
        self._n_pole = n_pole
        self._n_phase = n_phase
        self._n_rotor_slot = n_rotor_slot
        self._voltage_input = voltage_input
        self._frequency = frequency
        self._rotor_radius = rotor_radius
        self._lz_machine = lz_machine
        self._n_rotor_turns = n_rotor_turns
        self._rotor_wire = rotor_wire
        self._stator_winding = stator_winding
        self._rotor_power = rotor_power
        self._winding_factor = WindingFactor(self._stator_winding.get_n_slot_per_pole_per_phase, 1, self._stator_winding.get_n_turns)
        self._rotor_winding = Winding(self._n_pole, self._n_phase, self._n_rotor_slot, 0, self._lz_machine, self._rotor_radius, self._n_rotor_turns)

    @property
    def n_rotor_conductors(self):
        return self._n_rotor_conductors

    @property
    def get_rotor_winding(self):
        return self._rotor_winding

    #@property
    #def get_n_series_conductors_per_phase(self):
    #    return (0.97*self._voltage_input/np.sqrt(3)) / (2.22 * self._frequency * self.get_rotor_flux_per_pole * self._stator_winding.get_winding_distribution_factor * self._stator_step_factor)

    @property
    def get_single_rotor_turn_length(self):
        return 2*self._lz_machine + 4*self._rotor_radius

    @property
    def get_total_rotor_turn_length(self):
        return self.get_single_rotor_turn_length*self._n_rotor_turns

    @property
    def get_rotor_resistance(self):
        return Resistance_via_LS(self._rotor_wire.get_rho, self._rotor_winding.get_all_coil_length, self._rotor_wire.get_section)


    @property
    def get_rotor_resistance_ref_stator(self):
        return Resistance_from_value((self._stator_winding.get_n_turns / self._rotor_winding.get_n_turns)** 2 * self.get_rotor_resistance.get_value)