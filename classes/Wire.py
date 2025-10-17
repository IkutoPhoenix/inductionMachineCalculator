import numpy as np
from classes.Rho import Rho

class Wire:

    def __init__(self, D_wire: float, rho: Rho):
        self._D_wire = D_wire
        self._rho = rho

    @property
    def get_section(self):
        return np.pi * self._D_wire ** 2 / 4

    @property
    def get_rho(self):
        return self._rho