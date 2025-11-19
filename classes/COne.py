class COne:

    def __init__(self, n_pole: int):
        self._n_pole = n_pole
        self._values = [0, 3.65, 2.55, 2.20, 2, 1.9, 1.8, 1.73, 1.68]

    @property
    def get_value(self):
        return self._values[self._n_pole//2]