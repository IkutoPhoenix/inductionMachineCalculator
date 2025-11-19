from abc import ABC, abstractmethod
from AmpTheorem import *
from classes.Coefs import *
from classes.MagneticParameters import *


class Current(ABC):

    @property
    @abstractmethod
    def get_value(self):
        pass

class MagnetizingCurrent(Current):

    def __init__(self, magnetic_field_strength: list[MagneticParameters], lengths: list[float], n_poles: int, n_stator_turns: int, n_slot_per_pole_per_phase: int, shortening: float, n_turns: int):
        self._magnetic_field_strength = magnetic_field_strength
        self._lengths = lengths
        self._n_poles = n_poles
        self._n_stator_turns = n_stator_turns
        self._n_slot_per_pole_per_phase = n_slot_per_pole_per_phase
        self._shortening = shortening
        self._n_turns = n_turns
        self._winding_factor = WindingFactor(self._n_slot_per_pole_per_phase, self._shortening, self._n_turns)
        self._amp_theorem = AmpTheorem(self._lengths, self._lengths)

    @property
    def get_current_per_turns_per_pole(self):
        return self._amp_theorem.get_enclosed_current

    @property
    def get_value(self):
        return self._n_poles * np.pi * self.get_current_per_turns_per_pole / (3*np.sqrt(2) * self._winding_factor.get_value * self._n_turns)