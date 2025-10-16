from classes.Rho import *
from classes.WireSection import WireSection

Lz_machine = 0.3
N_slot = 10
N_phases = 3
Temperature_celsius = 20
D_wire = 0.001

S_coil_wire = WireSection(D_wire).get_value()