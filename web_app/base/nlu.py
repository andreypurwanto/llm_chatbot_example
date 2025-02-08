from abc import ABC, abstractmethod

class BaseNLUModel(ABC):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def prediction_result(self):
        pass

    @property
    @abstractmethod
    def predict_arg(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def postprocessing(self):
        pass