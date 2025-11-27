import numpy as np

class AmpTheorem:

    def __init__(self, magnetic_field_strength, magnetic_circuit_length):
        self._magnetic_field_strength = np.array(magnetic_field_strength)
        self._magnetic_circuit_length = np.transpose(np.array(magnetic_circuit_length))

    @property
    def get_enclosed_current(self):
        """ Return the Ampere's law I = H*L, I is a scalar"""
        return np.matmul(self._magnetic_field_strength, self._magnetic_circuit_length)

    @property
    def get_enclosed_current_array(self):
        return self._magnetic_field_strength*np.transpose(self._magnetic_circuit_length)