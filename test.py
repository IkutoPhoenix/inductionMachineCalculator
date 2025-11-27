from classes.Resistance import Resistance_via_LS
from classes.Rho import *
from classes.Wire import Wire
from classes.Winding import *

import tkinter as tk
from tkinter import ttk

lz_machine = 0.122
n_slot = 54
n_phase = 3
n_pole = 3
n_turns = 14
narrowing = 0
bore_radius = .267/2
temperature_celsius = 20
D_wire = 0.0029

stator_coil_wire = Wire(D_wire, Rho_Cu(temperature_celsius))
winding = Winding(n_pole, n_phase, n_slot, narrowing, lz_machine, bore_radius, n_turns)
stator_resistance = Resistance_via_LS(stator_coil_wire.get_rho, winding.get_all_coil_length, stator_coil_wire.get_section)

print(stator_resistance.get_value)