from abc import ABC, abstractmethod
import numpy as np
from scipy.interpolate import interp1d, CubicSpline

class BOfH(ABC):

    @abstractmethod
    def get_magnetic_flux_density(self, magnetic_field_strength):
        pass

    @abstractmethod
    def get_magnetic_field_strength(self, magnetic_flux_density):
        pass

class BOfH_M235_35A(BOfH):

    def __init__(self):
        self._data = np.loadtxt("data/BOfH_M235_35A.txt")
        self._h, self._b = self._data
        self._b_of_h_spline = CubicSpline(self._h, self._b, extrapolate=True)
        self._h_of_b_spline = CubicSpline(self._b, self._h, extrapolate=True)

    def get_magnetic_flux_density(self, magnetic_field_strength):
        return self._b_of_h_spline(magnetic_field_strength)

    def get_magnetic_field_strength(self, magnetic_flux_density):
        return self._h_of_b_spline(magnetic_flux_density)