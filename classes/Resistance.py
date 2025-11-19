import numpy as np
from classes.Rho import Rho
from abc import ABC, abstractmethod

class Resistance(ABC):

    @property
    @abstractmethod
    def get_value(self):
        pass

class Resistance_from_value(Resistance):

    def __init__(self, value: float):
        self._value = value

    @property
    def get_value(self):
        return self._value

class Resistance_via_LS(Resistance):

    def __init__(self, Rho: Rho, Length: float, Section: float):
        self._Rho = Rho # Conductivity
        self._Length = Length
        self._Section = Section

    @property
    def get_value(self):
        return self._Rho.get_value * self._Length / self._Section