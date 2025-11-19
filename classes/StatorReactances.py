

class StatorReactances():

    def __init__(self, n_stator_turns, n_phases, frequency, stator_winding, n_pole, stator_slot_width, stator_slot_height):
        self.n_stator_turns = n_stator_turns
        self.n_phases = n_phases
        self.frequency = frequency
        self.stator_winding = stator_winding
        self.n_pole = n_pole
        self.stator_slot_width = stator_slot_width
        self.stator_slot_height = stator_slot_height

        self._step_factor = 1
        pass

    def slot_factor(self):
        return


