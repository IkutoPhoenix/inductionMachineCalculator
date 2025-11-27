import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from classes.BOfH import BOfH_M235_35A
from classes.MagneticCircuit import MagneticCircuit
from classes.Reactance import MagnetizingReactance, ImpedanceFromValue
from classes.Rho import *
from classes.Rotor import *
from classes.SeriesReactances import SeriesReactance
from classes.MachinePerformance import MachinePerformance
from classes.MachineParameters import Machine

class StatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Base window settings
        self.title("Super Mega Motor Calculator 4000")
        self.geometry("1000x800")
        self.resizable(False, False)

        # Variables creation
        # ----- Stator
        self.var_n_stator_slot = tk.IntVar(value=54)
        self.var_n_stator_turns = tk.IntVar(value=126)
        self.var_narrowing = tk.IntVar(value=0)
        self.var_d_stator_wire = tk.DoubleVar(value=0.0029)
        self.var_stator_slot_width = tk.DoubleVar(value=0.267*3.14/54/2)
        self.var_stator_slot_length = tk.DoubleVar(value=0.04)
        self.var_stator_yoke_thickness = tk.DoubleVar(value=0.1)
        # ----- Rotor
        self.var_rotor_radius = tk.DoubleVar(value=0.2658 / 2)
        self.var_n_rotor_slot = tk.IntVar(value=45)
        self.var_n_rotor_turns = tk.IntVar(value=250)
        self.var_d_rotor_wire = tk.DoubleVar(value=0.006)
        self.var_rotor_power = tk.DoubleVar(value=18000)
        self.var_rotor_slot_width = tk.DoubleVar(value=0.2658*3.14/44/2)
        self.var_rotor_slot_length = tk.DoubleVar(value=0.03)
        self.var_rotor_yoke_thickness = tk.DoubleVar(value=0.08)
        # ----- Global
        self.var_n_phase = tk.IntVar(value=3)
        self.var_n_pole = tk.IntVar(value=3)
        self.var_lz_machine = tk.DoubleVar(value=0.122)
        self.var_bore_radius = tk.DoubleVar(value=0.267 / 2)
        self.var_temperature_celsius = tk.DoubleVar(value=20)
        self.var_voltage_input = tk.DoubleVar(value=230)
        self.var_frequency = tk.DoubleVar(value=50)
        self.var_air_gap_length = tk.DoubleVar(value=0.0015)
        self.var_slip = tk.DoubleVar(value=0.95)
        # ----- Other
        self.var_tolerance = tk.DoubleVar(value=0.01)
        self.var_max_iter = tk.DoubleVar(value=500)
        self.var_delta_B = tk.DoubleVar(value=0.04)

        # ----- Widget creation
        main = ttk.Frame(self, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        # Label and textbox array
        labelsGrid = [
            [
                ("==== STATOR ====", None),
                ("Nb of slot", self.var_n_stator_slot),
                ("Nb of turns per coil", self.var_n_stator_turns),
                ("Coil wire diameter (m)", self.var_d_stator_wire),
                ("Slot width (m)", self.var_stator_slot_width),
                ("Slot length (m)", self.var_stator_slot_length),
                ("Slot yoke thickness (m)", self.var_stator_yoke_thickness),
                ("===== ROTOR =====", None),
                ("Nb of slot", self.var_n_rotor_slot),
                ("Nb of turns per coil", self.var_n_rotor_turns),
                ("Coil wire diameter (m)", self.var_d_rotor_wire),
                ("Rotor radius (m)", self.var_rotor_radius),
                ("Rotor power (W)", self.var_rotor_power),
                ("Slot width (m)", self.var_rotor_slot_width),
                ("Slot length (m)", self.var_rotor_slot_length),
                ("Slot yoke thickness (m)", self.var_rotor_yoke_thickness),
            ],[
                ("===== GLOBAL =====", None),
                ("Machine length (m)", self.var_lz_machine),
                ("Nb of phase", self.var_n_phase),
                ("Nb of pair of pole", self.var_n_pole),
                ("Narrowing (0/1)", self.var_narrowing),
                ("Bore radius (m)", self.var_bore_radius),
                ("Temperature (°C)", self.var_temperature_celsius),
                ("Voltage input (V)", self.var_voltage_input),
                ("Frequency (Hz)", self.var_frequency),
                ("N of rotor turns", self.var_n_rotor_turns),
                ("Air gap length (m)", self.var_air_gap_length),
                ("Slip", self.var_slip),
            ],
            [
                ("===== CALCULATION =====", None),
                ("Tolerance", self.var_tolerance),
                ("Max. iterations", self.var_max_iter),
                ("Be incr. (T)", self.var_delta_B),
            ]
        ]

        # ---- Auto create grid from the array
        for ydx, (labels) in enumerate(labelsGrid):
            for idx, (text, var) in enumerate(labels):
                ttk.Label(main, text=text).grid(row=idx, column=0 + ydx*2, sticky="w", pady=4)
                if var is not None:
                    ttk.Entry(main, textvariable=var, width=12).grid(row=idx, column=1 + ydx*2, padx=8)

        # Get settings for the grid
        length = max([len(sub_array) for sub_array in labelsGrid])
        width = len(labelsGrid)*2

        ttk.Separator(main, orient="horizontal").grid(
            row=length, column=0, columnspan=width, sticky="ew", pady=12
        )

        ttk.Button(main, text="Calculate", command=self.calculate).grid(
            row=length + 1, column=1, columnspan=2, pady=12
        )
        ttk.Button(main, text="Torque Curve", command=lambda: self.calculate(option=2)).grid(
            row=length + 1, column=3, columnspan=2, pady=12
        )

        ttk.Label(main, text=text).grid(row=idx, column=0 + ydx * 2, sticky="w", pady=4)

        self.result = tk.Text(main, height=19, width=60, wrap="word")
        self.result.grid(row=length + 2, column=0, columnspan=width//2, pady=4)
        self.BTable = tk.Text(main, height=19, width=78, wrap="word")
        self.BTable.grid(row=length + 2, column=width//2, columnspan=width//2, pady=4)

    def calculate(self, option=1):
        #try:
        lz_machine = self.var_lz_machine.get()
        n_phase = self.var_n_phase.get()
        n_pole = self.var_n_pole.get()
        n_stator_slot = self.var_n_stator_slot.get()
        n_stator_turns = self.var_n_stator_turns.get()
        stator_slot_width = self.var_stator_slot_width.get()
        stator_slot_length = self.var_stator_slot_length.get()
        stator_yoke_thickness = self.var_stator_yoke_thickness.get()
        narrowing = self.var_narrowing.get()
        bore_radius = self.var_bore_radius.get()
        temperature_celsius = self.var_temperature_celsius.get()
        d_stator_wire = self.var_d_stator_wire.get()
        voltage_input = self.var_voltage_input.get()
        frequency = self.var_frequency.get()
        rotor_radius = self.var_rotor_radius.get()
        n_rotor_slot = self.var_n_rotor_slot.get()
        n_rotor_turns = self.var_n_rotor_turns.get()
        rotor_power = self.var_rotor_power.get()
        d_rotor_wire = self.var_d_rotor_wire.get()
        rotor_slot_width = self.var_rotor_slot_width.get()
        rotor_slot_length = self.var_rotor_slot_length.get()
        rotor_yoke_thickness = self.var_rotor_yoke_thickness.get()
        air_gap_length = self.var_air_gap_length.get()
        slip = self.var_slip.get()
        tolerance = self.var_tolerance.get()
        max_iterations = self.var_max_iter.get()
        delta_B = self.var_delta_B.get()

        machine = Machine(lz_machine, n_phase, n_pole, n_stator_slot, n_stator_turns, narrowing, bore_radius, temperature_celsius, d_stator_wire, voltage_input, frequency, rotor_radius, n_rotor_slot, n_rotor_turns, rotor_power, d_rotor_wire)

        # Stator resistance
        stator_coil_wire = Wire(d_stator_wire, Rho_Cu(temperature_celsius))
        stator_winding = Winding(n_pole, n_phase, n_stator_slot, narrowing, lz_machine, bore_radius, n_stator_turns)
        stator_resistance = Resistance_via_LS(
            stator_coil_wire.get_rho, stator_winding.get_all_coil_length, stator_coil_wire.get_section
        )

        # Rotor resistance
        rotor_coil_wire = Wire(d_rotor_wire, Rho_Cu(temperature_celsius))
        rotor = WoundRotor(n_pole, n_phase, n_rotor_slot, voltage_input, frequency, rotor_radius, lz_machine, n_rotor_turns, rotor_power, rotor_coil_wire, stator_winding)

        voltage_input_reverse = 0
        i = 0
        gap_magnetic_flux_density = 0.1
        while i < max_iterations and abs(voltage_input - voltage_input_reverse) > tolerance * voltage_input:
            i += 1
            magnetic_circuit = MagneticCircuit(gap_magnetic_flux_density, bore_radius, n_pole, lz_machine, BOfH_M235_35A(), n_stator_slot, n_rotor_slot, stator_yoke_thickness, rotor_yoke_thickness, stator_slot_width, rotor_slot_width, stator_slot_length, rotor_slot_length)
            magnetizing_reactance = MagnetizingReactance(magnetic_circuit, frequency, stator_winding, air_gap_length)

            stator_reactance = SeriesReactance(n_phase, frequency, stator_winding, n_pole, stator_slot_width, stator_slot_length, lz_machine, magnetizing_reactance, air_gap_length, voltage_input)
            rotor_reactance = SeriesReactance(n_phase, frequency, rotor.get_rotor_winding, n_pole, rotor_slot_width, rotor_slot_length, lz_machine, magnetizing_reactance, air_gap_length, voltage_input)

            stator_impedance = ImpedanceFromValue(stator_resistance.get_value + stator_reactance.get_reactance.get_value*1j)
            rotor_impedance = ImpedanceFromValue(rotor.get_rotor_resistance_ref_stator.get_value/slip + rotor_reactance.get_reactance.get_value*1j)
            magnetizing_impedance = ImpedanceFromValue(magnetizing_reactance.get_value*1j)
            voltage_input_reverse = np.abs(magnetizing_reactance.get_electromotrice_force * (1 + stator_impedance.get_value*(1/rotor_impedance.get_value + 1/magnetizing_impedance.get_value)))

            print(f"Iter {i:03d} | Be = {gap_magnetic_flux_density:.4f} T | Vn = {voltage_input_reverse:.2f} V | Erreur = {abs(voltage_input_reverse - voltage_input) / voltage_input * 100:.2f}%")
            if abs(voltage_input - voltage_input_reverse) <= tolerance * voltage_input:
                break

            if voltage_input_reverse < voltage_input:
                gap_magnetic_flux_density += delta_B
            else:
                gap_magnetic_flux_density -= delta_B / 2

        machine_performance = MachinePerformance(machine, stator_resistance, rotor, stator_reactance.get_reactance, magnetizing_reactance)

        if option == 1:
            out = (
                  f"===== RESULT FOR slip={slip:.3f} =====\n"
                + f"Stator resistance                 : {stator_resistance.get_value:.3f} Ω\n"
                + f"Rotor resistance                  : {rotor.get_rotor_resistance.get_value:.3f} Ω\n"
                + f"Rotor resistance from stator      : {rotor.get_rotor_resistance_ref_stator.get_value:.3f} Ω\n\n"
                + f"Magnetizing Reactance             : {magnetizing_reactance.get_value:.3f} Ω\n\n"
                + f"Stator Reactance                  : {stator_reactance.get_reactance.get_value:.3f} Ω\n"
                + f"-> Differential Leakage Reactance : {stator_reactance.get_differential_leakage_reactance.get_value:.3f} Ω\n"
                + f"-> Slot Leakage Reactance         : {stator_reactance.get_slot_leakage_reactance.get_value:.3f} Ω\n"
                + f"-> Loop Leakage Reactance         : {stator_reactance.get_loop_leakage_reactance.get_value:.3f} Ω\n\n"
                + f"Rotor Reactance                   : {rotor_reactance.get_reactance.get_value:.3f} Ω\n"
                + f"-> Differential Leakage Reactance : {rotor_reactance.get_differential_leakage_reactance.get_value:.3f} Ω\n"
                + f"-> Slot Leakage Reactance         : {rotor_reactance.get_slot_leakage_reactance.get_value:.3f} Ω\n"
                + f"-> Loop Leakage Reactance         : {rotor_reactance.get_loop_leakage_reactance.get_value:.3f} Ω"
            )
            self.result.delete("1.0", tk.END)
            self.result.insert(tk.END, out)

            out2 = (
                  f"===== RESULT FOR slip={slip:.3f} =====\n"
                + f"Starting torque : {machine_performance.starting_torque:.3f}\n"
                + f"Slip at maximum torque : {machine_performance.slip_at_maximum_torque:.3f}\n"
                + f"Maximum torque : {machine_performance.maximum_torque:.3f}\n\n"
                + f"+--------------+------------------+----------------------+------------------+\n"
                + f"|              | Flux Density (T) | Field Strength (A/m) | Amp. Turns (AT)  |\n"
                + f"+--------------+------------------+----------------------+------------------+\n"
                + f"| Air gap      | {magnetic_circuit.get_gap_magnetic_flux_density.get_magnetic_flux_density:>16.3e} | {magnetic_circuit.get_gap_magnetic_flux_density.get_magnetic_field_strength:>20.3e} | {magnetic_circuit.get_gap_magnetic_flux_density.get_magnetic_field_strength:>16.3e} |\n"
                + f"| Stator yoke  | {magnetic_circuit.get_stator_yoke_magnetic_flux_density.get_magnetic_flux_density:>16.3e} | {magnetic_circuit.get_stator_yoke_magnetic_flux_density.get_magnetic_field_strength:>20.3e} | {magnetic_circuit.get_gap_magnetic_flux_density.get_magnetic_field_strength:>16.3e} |\n"
                + f"| Stator teeth | {magnetic_circuit.get_stator_teeth_magnetic_flux_density.get_magnetic_flux_density:>16.3e} | {magnetic_circuit.get_stator_teeth_magnetic_flux_density.get_magnetic_field_strength:>20.3e} | {magnetic_circuit.get_gap_magnetic_flux_density.get_magnetic_field_strength:>16.3e} |\n"
                + f"| Rotor  yoke  | {magnetic_circuit.get_rotor_yoke_magnetic_flux_density.get_magnetic_flux_density:>16.3e} | {magnetic_circuit.get_rotor_yoke_magnetic_flux_density.get_magnetic_field_strength:>20.3e} | {magnetic_circuit.get_gap_magnetic_flux_density.get_magnetic_field_strength:>16.3e} |\n"
                + f"| Rotor  teeth | {magnetic_circuit.get_rotor_teeth_magnetic_flux_density.get_magnetic_flux_density:>16.3e} | {magnetic_circuit.get_rotor_teeth_magnetic_flux_density.get_magnetic_field_strength:>20.3e} | {magnetic_circuit.get_gap_magnetic_flux_density.get_magnetic_field_strength:>16.3e} |\n"
                + f"+--------------+------------------+----------------------+------------------+"
            )
            self.BTable.delete("1.0", tk.END)
            self.BTable.insert(tk.END, out2)
        elif option == 2:
            torque_curve = machine_performance.compute_torque_curve()
            plt.plot(torque_curve[0], torque_curve[2], 'r')
            plt.xlabel("slip")
            plt.ylabel("torque (Nm)")
            plt.title("Machine Performance - Torque Curve")
            plt.show()


app = StatorApp()
app.mainloop()
