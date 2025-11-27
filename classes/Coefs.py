from abc import ABC, abstractmethod
import numpy as np
from classes.Winding import *

"""
Type of class to compute and get specific coefficient
"""

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

class CorrectionFactor(Coef):

    def __init__(self, n_poles: int, inner_diameter: float, rotor_radius: float):
        self._n_poles = n_poles
        self._inner_diameter = inner_diameter
        self._outer_diameter = rotor_radius*2
        self._diameter_ratio = self._inner_diameter / self._outer_diameter

    @property
    def get_value(self):
        val_matrix = np.array([[1.0906, -0.8531, 0.6161, -0.13105, 0.01308, -0.0004519], [1.1370, -1.1690, 0.04730, 0.03300, -0.008128, 0.0003807], [-1.2310, 3.3130, -1.5255, 0.2838, -0.02135, 0.0005869], [0.06021, -1.3575, 0.8910, -0.1914, 0.01688, -0.0005308]])
        p_matrix = np.transpose(np.array([1, self._n_poles, self._n_poles**2, self._n_poles**3, self._n_poles**4, self._n_poles**5]))
        ratio_matrix = np.transpose(np.array([1, self._diameter_ratio, self._diameter_ratio**2, self._diameter_ratio**3]))
        return np.matmul(np.matmul(val_matrix, p_matrix), ratio_matrix)
