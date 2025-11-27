import numpy as np
from classes.MachineParameters import Machine
from classes.Reactance import *
from classes.Rotor import *

class MachinePerformance:
    """
    Compute induction machine performance from electrical parameters and slip.
    """

    def __init__(self, machine: Machine, stator_resistance: Resistance, rotor: Rotor, stator_reactance: Reactance, magnetizing_reactance: Reactance):
        # -----------------------------
        # Electrical machine parameters
        # -----------------------------
        self.phase_voltage = machine.get_voltage_input / np.sqrt(3)

        self.stator_resistance = stator_resistance.get_value
        self.rotor_resistance_ref_stator = rotor.get_rotor_resistance_ref_stator.get_value

        # Reactances (standard names from your architecture)
        self.stator_reactance = stator_reactance.get_value
        self.rotor_reactance = stator_reactance.get_value
        self.magnetizing_reactance = magnetizing_reactance.get_value

        # -----------------------------
        # Machine mechanical parameters
        # -----------------------------
        self.n_poles = machine.get_n_pole
        self.frequency = machine.get_frequency

        # Synchronous speed
        self.pair_of_poles = self.n_poles / 2
        self.synchronous_speed_rpm = 60 * self.frequency / self.pair_of_poles
        self.synchronous_speed_rad_s = self.synchronous_speed_rpm * np.pi / 30

    # ----------------------------------------------------------------------
    # Compute performance quantities at a given slip "s"
    # ----------------------------------------------------------------------
    def compute_performance_at_slip(self, slip):
        jXs = 1j * self.stator_reactance
        jXr = 1j * self.rotor_reactance
        jXm = 1j * self.magnetizing_reactance

        # Rotor resistance divided by slip
        rotor_resistance_slip = self.rotor_resistance_ref_stator / slip

        # Impedances
        Z_magnetizing = jXm
        Z_rotor = rotor_resistance_slip + jXr
        Z_stator = self.stator_resistance + jXs

        # Equivalent impedance at stator
        Z_eq = Z_stator + (Z_magnetizing * Z_rotor) / (Z_magnetizing + Z_rotor)

        stator_current = self.phase_voltage / Z_eq
        internal_emf = self.phase_voltage - Z_stator * stator_current
        magnetizing_current = internal_emf / Z_magnetizing
        rotor_current = stator_current - magnetizing_current

        # Power transferred to rotor
        apparent_power_transferred = 3 * internal_emf * np.conj(rotor_current)
        active_power_transferred = np.real(apparent_power_transferred)

        electromagnetic_torque = active_power_transferred / self.synchronous_speed_rad_s

        mechanical_speed_rpm = (1 - slip) * self.synchronous_speed_rpm

        # Power factor
        power_factor = np.cos(np.angle(stator_current))

        # Mechanical output power
        output_power = electromagnetic_torque * mechanical_speed_rpm * (np.pi / 30)

        # Input power
        input_power = 3 * self.phase_voltage * abs(stator_current) * power_factor

        # Efficiency
        efficiency = output_power / input_power if input_power != 0 else 0

        # Copper losses
        stator_copper_loss = 3 * self.stator_resistance * (abs(stator_current) ** 2)
        rotor_copper_loss = 3 * self.rotor_resistance_ref_stator * (abs(rotor_current) ** 2)

        return {
            "slip": slip,
            "speed_rpm": mechanical_speed_rpm,
            "stator_current": stator_current,
            "rotor_current": rotor_current,
            "magnetizing_current": magnetizing_current,
            "electromagnetic_torque": electromagnetic_torque,
            "output_power": output_power,
            "input_power": input_power,
            "stator_copper_loss": stator_copper_loss,
            "rotor_copper_loss": rotor_copper_loss,
            "power_factor": power_factor,
            "efficiency": efficiency,
        }

    # ----------------------------------------------------------------------
    # Torque vs slip curve
    # ----------------------------------------------------------------------
    def compute_torque_curve(self, N=2000):
        slip_values = np.linspace(0.001, 1, N)
        torque_values = np.zeros_like(slip_values)
        speed_values = (1 - slip_values) * self.synchronous_speed_rpm

        for i in range(N):
            torque_values[i] = self.compute_performance_at_slip(slip_values[i])["electromagnetic_torque"]

        return slip_values, speed_values, torque_values

    # ----------------------------------------------------------------------
    # Machine operating point at given load torque
    # ----------------------------------------------------------------------
    def get_operating_point(self, load_torque):
        slip_values, _, torque_values = self.compute_torque_curve()
        idx = np.argmin(np.abs(torque_values - load_torque))

        perf = self.compute_performance_at_slip(slip_values[idx])
        perf["load_torque"] = load_torque

        return perf

    # ----------------------------------------------------------------------
    # Key torque characteristics
    # ----------------------------------------------------------------------
    @property
    def maximum_torque(self):
        _, _, torque_values = self.compute_torque_curve()
        return np.max(torque_values)

    @property
    def slip_at_maximum_torque(self):
        slip_values, _, torque_values = self.compute_torque_curve()
        return slip_values[np.argmax(torque_values)]

    @property
    def starting_torque(self):
        return self.compute_performance_at_slip(1)["electromagnetic_torque"]

    @property
    def starting_current(self):
        """Stator current at starting conditions (slip = 1)."""
        return self.compute_performance_at_slip(1)["stator_current"]