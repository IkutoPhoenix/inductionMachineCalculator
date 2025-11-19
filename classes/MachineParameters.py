from scipy.special import erf_zeros


class Machine:

    def __init__(self, lz_machine: float, n_phase: int, n_pole: int, n_stator_slot: int, n_stator_turns: int, narrowing: float, bore_radius: float, temperature_celsius: float, d_stator_wire: float, voltage_input: float, frequency: float, rotor_radius: float, n_rotor_slot: int, n_rotor_turns: int, rotor_power: float, d_rotor_wire: float):
        self.__lz_machine = lz_machine
        self.__n_phase = n_phase
        self.__n_pole = n_pole
        self.__n_stator_slot = n_stator_slot
        self.__n_stator_turns = n_stator_turns
        self.__narrowing = narrowing
        self.__bore_radius = bore_radius
        self.__temperature_celsius = temperature_celsius
        self.__d_stator_wire = d_stator_wire
        self.__voltage_input = voltage_input
        self.__frequency = frequency
        self.__rotor_radius = rotor_radius
        self.__n_rotor_slot = n_rotor_slot
        self.__n_rotor_turns = n_rotor_turns
        self.__rotor_power = rotor_power
        self.__d_rotor_wire = d_rotor_wire

    @property
    def get_lz_machine(self):
        return self.__lz_machine

    @property
    def get_n_phase(self):
        return self.__n_phase

    @property
    def get_n_pole(self):
        return self.__n_pole

    @property
    def get_n_stator_slot(self):
        return self.__n_stator_slot

    @property
    def get_n_stator_turns(self):
        return self.__n_stator_turns

    @property
    def get_narrowing(self):
        return self.__narrowing

    @property
    def get_bore_radius(self):
        return self.__bore_radius

    @property
    def get_temperature_celsius(self):
        return self.__temperature_celsius

    @property
    def get_d_stator_wire(self):
        return self.__d_stator_wire

    @property
    def get_voltage_input(self):
        return self.__voltage_input

    @property
    def get_frequency(self):
        return self.__frequency

    @property
    def get_rotor_radius(self):
        return self.__rotor_radius

    @property
    def get_n_rotor_slot(self):
        return self.__n_rotor_slot

    @property
    def get_n_rotor_turns(self):
        return self.__n_rotor_turns

    @property
    def get_rotor_power(self):
        return self.__rotor_power

    @property
    def get_d_rotor_wire(self):
        return self.__d_rotor_wire