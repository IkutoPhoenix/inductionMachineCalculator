from abc import ABC, abstractmethod

from classes.AmpTheorem import AmpTheorem
from classes.MagneticCircuit import MagneticCircuit
import numpy as np
from classes.Coefs import *

class Reactance(ABC):

    @property
    @abstractmethod
    def get_value(self):
        pass

class ReactanceFromValue(Reactance):

    def __init__(self, value):
        self._value = value

    @property
    def get_value(self):
        return self._value

class MagnetizingReactance(Reactance):

    def __init__(self, magnetic_circuit: MagneticCircuit, frequency: float, stator_winding: Winding, air_gap_length: float):
        self._magnetic_circuit = magnetic_circuit
        self._frequency = frequency
        self._stator_winding = stator_winding
        self._air_gap_length = air_gap_length
        self._electromotrice_force = 2 * np.pi * WindingFactor(self._stator_winding.get_n_slot_per_pole_per_phase, 1, self._stator_winding.get_n_turns).get_value * self._frequency * self._stator_winding.get_n_turns * self._magnetic_circuit.get_pole_magnetic_flux / np.sqrt(2)
        field_strenghs = np.array([self._magnetic_circuit.get_stator_yoke_magnetic_flux_density.get_magnetic_field_strength, self._magnetic_circuit.get_stator_teeth_magnetic_flux_density.get_magnetic_field_strength, self._magnetic_circuit.get_rotor_yoke_magnetic_flux_density.get_magnetic_field_strength, self._magnetic_circuit.get_rotor_teeth_magnetic_flux_density.get_magnetic_field_strength, self._magnetic_circuit.get_gap_magnetic_flux_density.get_magnetic_field_strength])
        stator_yoke_path = self._magnetic_circuit.get_stator_yoke_thickness + (self._magnetic_circuit.get_bore_radius + self._magnetic_circuit.get_stator_slot_length + self._magnetic_circuit.get_stator_yoke_thickness/2)*(self._stator_winding.get_pole_pitch/2)
        rotor_yoke_path = self._magnetic_circuit.get_rotor_yoke_thickness + (self._magnetic_circuit.get_bore_radius - self._magnetic_circuit.get_rotor_slot_length - self._magnetic_circuit.get_rotor_yoke_thickness/2)*(self._stator_winding.get_pole_pitch/2)
        lengths = np.array([stator_yoke_path, 2*self._magnetic_circuit.get_stator_slot_length, rotor_yoke_path, 2*self._magnetic_circuit.get_rotor_slot_length, 2*self._air_gap_length])
        self._magnetizing_current = self._stator_winding.get_n_pole * np.pi * AmpTheorem(field_strenghs, lengths).get_enclosed_current / (3*np.sqrt(2)*WindingFactor(self._stator_winding.get_n_slot_per_pole_per_phase, 1, self._stator_winding.get_n_turns).get_value*self._stator_winding.get_n_turns)
        self._value = self._electromotrice_force/self._magnetizing_current


    @property
    def get_value(self):
        return self._value

    @property
    def get_magnetizing_current(self):
        return self._magnetizing_current

    @property
    def get_electromotrice_force(self):
        return self._electromotrice_force

class ImpedanceFromValue(Reactance):

    def __init__(self, value):
        self._value = value

    @property
    def get_value(self):
        return self._value