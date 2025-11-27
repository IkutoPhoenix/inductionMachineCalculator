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
        # Import B(H) table from txt
        self._data = np.loadtxt("data/bh_clean_M235_35A.txt")

        # Get arrays
        self._h, self._b = self._data.T

        # Get the extrapolation of the arrays
        self._b_of_h_spline = CubicSpline(self._h, self._b, extrapolate=True)
        self._h_of_b_spline = CubicSpline(self._b, self._h, extrapolate=True)

    def get_magnetic_flux_density(self, magnetic_field_strength):
        return self._b_of_h_spline(magnetic_field_strength)

    def get_magnetic_field_strength(self, magnetic_flux_density):
        return self._h_of_b_spline(magnetic_flux_density)

class BOfH_Air(BOfH):

    def __init__(self):
        # Air B(H) is linear with ~mu_0
        self._mu_0 = 4e-7 * np.pi

    def get_magnetic_flux_density(self, magnetic_field_strength):
        return self._mu_0 * magnetic_field_strength

    def get_magnetic_field_strength(self, magnetic_flux_density):
        return magnetic_flux_density / self._mu_0