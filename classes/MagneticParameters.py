from classes.BOfH import *

"""
Class for magnetic parameters to easily switch between B and H
"""

class MagneticParameters(ABC):

    @property
    @abstractmethod
    def get_magnetic_flux_density(self):
        pass

    @property
    @abstractmethod
    def get_magnetic_field_strength(self):
        pass

class MagneticParametersFromMagneticFluxDensity(MagneticParameters):

    def __init__(self, magnetic_flux_density, b_of_h: BOfH):
        self._magnetic_flux_density = magnetic_flux_density
        self._b_of_h = b_of_h
        self._magnetic_field_strength = self._b_of_h.get_magnetic_field_strength(self._magnetic_flux_density)

    @property
    def get_magnetic_field_strength(self):
        return self._magnetic_field_strength

    @property
    def get_magnetic_flux_density(self):
        return self._magnetic_flux_density

class MagneticParametersFromMagneticFieldStrength(MagneticParameters):

    def __init__(self, magnetic_field_strength, b_of_h: BOfH):
        self._magnetic_field_strength = magnetic_field_strength
        self._b_of_h = b_of_h
        self._magnetic_flux_density = self._b_of_h.get_magnetic_flux_density(self._magnetic_field_strength)

    @property
    def get_magnetic_field_strength(self):
        return self._magnetic_field_strength

    @property
    def get_magnetic_flux_density(self):
        return self._magnetic_flux_density