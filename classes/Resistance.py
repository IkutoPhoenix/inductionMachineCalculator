import numpy as np
from Rho import *
from abc import ABC, abstractmethod

class Resistance(ABC):

    @abstractmethod
    def get_value(self):
        pass

class Resistance_via_LS(Resistance):

    def __init__(self, Rho: Rho, Temperature_celsius: float, Length: float, Section: float):
        self._Rho = Rho
        self._Temperature_celsius = Temperature_celsius # (°C) Temperature
        self._Length = Length
        self._Section = Section

    def get_value(self):
        return self._Rho.get_value(T_kelvin=self._Temperature_celsius) * self._Length / self._Section