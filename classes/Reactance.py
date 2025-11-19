from abc import ABC, abstractmethod

class Reactance(ABC):

    @property
    @abstractmethod
    def get_value(self):
        pass

class ReactanceFromValue(Reactance):

    def __init__(self, value):
        self._value = value

    @property
    def get_value(self):
        return self._value