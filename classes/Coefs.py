from abc import ABC, abstractmethod
import numpy as np
from Winding import *

class Coef(ABC):

    @property
    @abstractmethod
    def get_value(self):
        pass

class FilteringFactor(Coef):

    def __init__(self, n_turns: int):
        self._n_turns = n_turns

    @property
    def get_value(self):
        return np.sin(np.pi/self._n_turns)/np.pi*self._n_turns

class ShortPitchFactor(Coef):

    def __init__(self, shortening):
        self._shortening = shortening

    @property
    def get_value(self):
        return np.sin(self._shortening/2)

class DistributionFactor(Coef):

    def __init__(self, n_slot_per_pole_per_phase: int, n_turns: int):
        self._n_slot_per_pole_per_phase = n_slot_per_pole_per_phase
        self._n_turns = n_turns

    @property
    def get_value(self):
        return np.sin(self._n_slot_per_pole_per_phase*np.pi/self._n_turns)/(self._n_slot_per_pole_per_phase * np.sin(np.pi/self._n_turns))

class WindingFactor(Coef):

    def __init__(self, n_slot_per_pole_per_phase: int, shortening: float, n_turns: int):
        self._n_turns = n_turns
        self._shortening = shortening
        self._n_slot_per_pole_per_phase = n_slot_per_pole_per_phase

        self._filtering_factor = FilteringFactor(n_turns)
        self._short_pitch_factor = ShortPitchFactor(shortening)
        self._distribution_factor = DistributionFactor(n_slot_per_pole_per_phase, n_turns)

    @property
    def get_value(self):
        return self._filtering_factor.get_value * self._short_pitch_factor.get_value * self._distribution_factor.get_value

class CarterCoefficient(Coef):
    def __init__(self, stator_slot_width: float, stator_winding: Winding, air_gap_length: float):
        self._stator_slot_width = stator_slot_width
        self._stator_winding = stator_winding
        self._air_gap_length = air_gap_length

    @property
    def get_value(self):
        return self._stator_winding.get_tooth_pitch/(self._stator_winding.get_tooth_pitch - self._stator_slot_width**2/(5*self._air_gap_length + self._stator_slot_width))
