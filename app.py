import tkinter as tk
from tkinter import ttk, messagebox

from classes.Resistance import Resistance_via_LS
from classes.Rho import *
from classes.Wire import Wire
from classes.Winding import *

class StatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Super Mega Motor Calculator 4000")
        self.geometry("420x520")
        self.resizable(False, False)

        # ------------------------------------------------------------------
        # Variables liées aux widgets
        # ------------------------------------------------------------------
        self.var_lz_machine = tk.DoubleVar(value=0.122)
        self.var_n_slot = tk.IntVar(value=54)
        self.var_n_phase = tk.IntVar(value=3)
        self.var_n_pole = tk.IntVar(value=3)
        self.var_n_turns = tk.IntVar(value=14)
        self.var_narrowing = tk.IntVar(value=0)
        self.var_bore_radius = tk.DoubleVar(value=0.267 / 2)
        self.var_temperature_celsius = tk.DoubleVar(value=20)
        self.var_d_wire = tk.DoubleVar(value=0.0029)

        # ------------------------------------------------------------------
        # Création des widgets
        # ------------------------------------------------------------------
        main = ttk.Frame(self, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        labels = [
            ("Longueur machine (m)", self.var_lz_machine),
            ("Nb of slot", self.var_n_slot),
            ("Nb of phase", self.var_n_phase),
            ("Nb of pole", self.var_n_pole),
            ("Nb of turns per coil", self.var_n_turns),
            ("Narrowing (0/1)", self.var_narrowing),
            ("Bore radius (m)", self.var_bore_radius),
            ("Temperature (°C)", self.var_temperature_celsius),
            ("Stator coil wire diameter (m)", self.var_d_wire),
        ]

        for idx, (text, var) in enumerate(labels):
            ttk.Label(main, text=text).grid(row=idx, column=0, sticky="w", pady=4)
            ttk.Entry(main, textvariable=var, width=12).grid(row=idx, column=1, padx=8)

        ttk.Separator(main, orient="horizontal").grid(
            row=len(labels), column=0, columnspan=2, sticky="ew", pady=12
        )

        ttk.Button(main, text="Calculer", command=self.calculate).grid(
            row=len(labels) + 1, column=0, columnspan=2, pady=12
        )

        self.result = tk.Text(main, height=8, width=45, wrap="word")
        self.result.grid(row=len(labels) + 2, column=0, columnspan=2, pady=8)

    def calculate(self):
        try:
            lz_machine = self.var_lz_machine.get()
            n_slot = self.var_n_slot.get()
            n_phase = self.var_n_phase.get()
            n_pole = self.var_n_pole.get()
            n_turns = self.var_n_turns.get()
            narrowing = self.var_narrowing.get()
            bore_radius = self.var_bore_radius.get()
            temperature_celsius = self.var_temperature_celsius.get()
            D_wire = self.var_d_wire.get()

            stator_coil_wire = Wire(D_wire, Rho_Cu(temperature_celsius))
            stator_winding = Winding(n_pole, n_phase, n_slot, narrowing, lz_machine, bore_radius, n_turns)
            stator_resistance = Resistance_via_LS(
                stator_coil_wire.get_rho, stator_winding.get_all_coil_length, stator_coil_wire.get_section
            )


            out = (
                f"Stator resistance : {stator_resistance.get_value:.3f} Ω"
            )
            self.result.delete("1.0", tk.END)
            self.result.insert(tk.END, out)

        except Exception as exc:
            messagebox.showerror("Erreur", str(exc))


app = StatorApp()
app.mainloop()