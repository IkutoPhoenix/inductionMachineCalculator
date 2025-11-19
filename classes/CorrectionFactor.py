import numpy as np

class CorrectionFactor:

    def __init__(self, n_poles: int, inner_diameter: float, rotor_radius: float):
        self._n_poles = n_poles
        self._inner_diameter = inner_diameter
        self._outer_diameter = rotor_radius*2
        self._diameter_ratio = self._inner_diameter / self._outer_diameter

    @property
    def get_value(self): #cf Conception de Moteurs Asynchrones p.90
        val_matrix = np.array([[1.0906, -0.8531, 0.6161, -0.13105, 0.01308, -0.0004519], [1.1370, -1.1690, 0.04730, 0.03300, -0.008128, 0.0003807], [-1.2310, 3.3130, -1.5255, 0.2838, -0.02135, 0.0005869], [0.06021, -1.3575, 0.8910, -0.1914, 0.01688, -0.0005308]])
        p_matrix = np.transpose(np.array([1, self._n_poles, self._n_poles**2, self._n_poles**3, self._n_poles**4, self._n_poles**5]))
        ratio_matrix = np.transpose(np.array([1, self._diameter_ratio, self._diameter_ratio**2, self._diameter_ratio**3]))
        return np.matmul(np.matmul(val_matrix, p_matrix), ratio_matrix)
