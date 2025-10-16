import numpy as np

class WireSection():

    def __init__(self, D_wire: float):
        self._D_wire = D_wire

    def get_value(self):
        return np.pi * self._D_wire ** 2 / 4