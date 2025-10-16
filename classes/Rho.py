from abc import ABC, abstractmethod

class Rho(ABC):

    def __init__(self, T_celsius):
        self._T_kelvin = T_celsius + 273.15
        self._alpha = None
        self._rho0 = None
        self._T0 = None

    @property
    def get_value(self): # Get the value of conductivity with
        return self._rho0 * (1 + self._alpha*(self._T_kelvin - self._T0))

class Rho_Cu(Rho): #Conductivity of copper

    def __init__(self, T_celsius):
        super().__init__(T_celsius)
        self._alpha = 4.04e-3 # (K-1) Temperature coefficient
        self._rho0 = 59.6e6 #(S/m) Conductivity at T0
        self._T0 = 20 + 273.15 #(K) Temperature of rho0