
class coil:

    def __init__(self, n_pole: int, n_phases: int, n_slots):
        self._n_pole = n_pole
        self._n_phases = n_phases
        self._n_slots = n_slots

    @property
    def get_n_slot_per_pole_per_phase(self):
        return self._n_slots / (2 * self._n_pole * self._n_phases)

    @property
    def get_n_spire_per_slot(self):
        return self._n_slots / (self._n_pole * self.get_n_slot_per_pole_per_phase)