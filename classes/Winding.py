import numpy as np

class Winding:

    def __init__(self, n_pole: int, n_phase: int, n_slot: int, narrowing: float, lz_machine: float, bore_radius: float, n_turns: float):
        self._n_pole = n_pole
        self._n_phase = n_phase
        self._n_slot = n_slot
        self._narrowing = narrowing
        self._lz_machine = lz_machine
        self._bore_radius = bore_radius
        self._n_turns = n_turns

    @property
    def get_n_slot_per_pole_per_phase(self): # Get the number of slot per pole per phase
        return self._n_slot / (2 * self._n_pole * self._n_phase)

    @property
    def get_n_spire_per_slot(self): # Get the number of spire per slot
        return self._n_slot / (self._n_pole * self.get_n_slot_per_pole_per_phase)

    @property
    def get_n_teeth(self): # Get the number of teeth
        return 2*self._n_pole * self._n_phase*self.get_n_slot_per_pole_per_phase

    @property
    def get_tooth_pitch(self): # Get the tooth pitch
        return 2*np.pi/self.get_n_teeth

    @property
    def get_pole_pitch(self): # Get the pole pitch
        return np.pi/self._n_pole

    @property
    def get_coil_span_angle(self): # Get coil span angle
        return (1 - self._narrowing / (self.get_n_slot_per_pole_per_phase * self._n_phase))*self.get_pole_pitch

    @property
    def get_single_turn_length(self):
        return 2*(self._lz_machine + self._bore_radius*self.get_coil_span_angle)

    @property
    def get_coil_length(self):
        return self.get_single_turn_length * self._n_turns

    @property
    def get_all_coil_length(self):
        return self.get_coil_length * self._n_pole