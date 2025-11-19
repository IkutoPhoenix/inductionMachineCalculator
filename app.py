import tkinter as tk
from tkinter import ttk, messagebox

from classes.MagneticCircuit import MagneticCircuit
from classes.Rho import *
from classes.Rotor import *

class StatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Super Mega Motor Calculator 4000")
        self.geometry("800x800")
        self.resizable(False, False)

        # ------------------------------------------------------------------
        # Variables liées aux widgets
        # ------------------------------------------------------------------
        # ----- Stator
        self.var_n_stator_slot = tk.IntVar(value=54)
        self.var_n_stator_turns = tk.IntVar(value=126)
        self.var_narrowing = tk.IntVar(value=0)
        self.var_d_stator_wire = tk.DoubleVar(value=0.0029)
        # ----- Rotor
        self.var_rotor_radius = tk.DoubleVar(value=0.2658 / 2)
        self.var_n_rotor_slot = tk.IntVar(value=44)
        self.var_n_rotor_turns = tk.IntVar(value=50)
        self.var_d_rotor_wire = tk.DoubleVar(value=0.0029)
        self.var_rotor_power = tk.DoubleVar(value=18000)
        # ----- Global
        self.var_n_phase = tk.IntVar(value=3)
        self.var_n_pole = tk.IntVar(value=3)
        self.var_lz_machine = tk.DoubleVar(value=0.122)
        self.var_bore_radius = tk.DoubleVar(value=0.267 / 2)
        self.var_temperature_celsius = tk.DoubleVar(value=20)
        self.var_voltage_input = tk.DoubleVar(value=230)
        self.var_frequency = tk.DoubleVar(value=50)

        # ------------------------------------------------------------------
        # Création des widgets
        # ------------------------------------------------------------------
        main = ttk.Frame(self, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        labelsGrid = [
            [
                ("==== STATOR ====", None),
                ("Nb of slot", self.var_n_stator_slot),
                ("Nb of turns per coil", self.var_n_stator_turns),
                ("Coil wire diameter (m)", self.var_d_stator_wire),
                ("===== ROTOR =====", None),
                ("Nb of slot", self.var_n_rotor_slot),
                ("Nb of turns per coil", self.var_n_rotor_turns),
                ("Coil wire diameter (m)", self.var_d_rotor_wire),
                ("Rotor radius (m)", self.var_rotor_radius),
                ("Rotor power (W)", self.var_rotor_power),
            ],[
                ("===== GLOBAL =====", None),
                ("Machine length (m)", self.var_lz_machine),
                ("Nb of phase", self.var_n_phase),
                ("Nb of pole", self.var_n_pole),
                ("Narrowing (0/1)", self.var_narrowing),
                ("Bore radius (m)", self.var_bore_radius),
                ("Temperature (°C)", self.var_temperature_celsius),
                ("Voltage input (V)", self.var_voltage_input),
                ("Frequency (Hz)", self.var_frequency),
                ("N of rotor turns", self.var_n_rotor_turns),
            ]
        ]

        for ydx, (labels) in enumerate(labelsGrid):
            for idx, (text, var) in enumerate(labels):
                ttk.Label(main, text=text).grid(row=idx, column=0 + ydx*2, sticky="w", pady=4)
                if var is not None:
                    ttk.Entry(main, textvariable=var, width=12).grid(row=idx, column=1 + ydx*2, padx=8)

        length = max([len(sub_array) for sub_array in labelsGrid])
        width = len(labelsGrid)*2

        ttk.Separator(main, orient="horizontal").grid(
            row=length, column=0, columnspan=width, sticky="ew", pady=12
        )

        ttk.Button(main, text="Calculate", command=self.calculate).grid(
            row=length + 1, column=0, columnspan=width, pady=12
        )

        self.result = tk.Text(main, height=8, width=45, wrap="word")
        self.result.grid(row=length + 2, column=0, columnspan=width, pady=8)

    def calculate(self):
        #try:
        lz_machine = self.var_lz_machine.get()
        n_phase = self.var_n_phase.get()
        n_pole = self.var_n_pole.get()
        n_stator_slot = self.var_n_stator_slot.get()
        n_stator_turns = self.var_n_stator_turns.get()
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

        # Stator resistance
        stator_coil_wire = Wire(d_stator_wire, Rho_Cu(temperature_celsius))
        stator_winding = Winding(n_pole, n_phase, n_stator_slot, narrowing, lz_machine, bore_radius, n_stator_turns)
        stator_resistance = Resistance_via_LS(
            stator_coil_wire.get_rho, stator_winding.get_all_coil_length, stator_coil_wire.get_section
        )

        # Rotor resistance
        rotor_coil_wire = Wire(d_rotor_wire, Rho_Cu(temperature_celsius))
        rotor = WoundRotor(n_pole, n_phase, n_rotor_slot, voltage_input, frequency, rotor_radius, lz_machine, n_rotor_turns, rotor_power, rotor_coil_wire, stator_winding)

        # Xm
        #magnetic_circuit = MagneticCircuit()
        #E = 2*np.pi*WindingFactor(stator_winding.get_n_slot_per_pole_per_phase, 1, n_stator_turns).get_value*frequency*n_stator_turns*magnetic_circuit.get_pole_magnetic_flux/np.sqrt(2)
        out = (
            f"Stator resistance : {stator_resistance.get_value:.3f} Ω\n"
            + f"Rotor resistance : {rotor.get_rotor_resistance.get_value:.3f} Ω\n"
            + f"Rotor resistance from stator : {rotor.get_rotor_resistance_ref_stator.get_value:.3f} Ω"
        )
        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, out)

        #except Exception as exc:
        #    messagebox.showerror("Erreur", str(exc))


app = StatorApp()
app.mainloop()
