from abc import abstractmethod
from configurations import Config

"""Abstract Model class that is inherited to all models
We have to thing about the functionalities before we dive into the code of the model."""
class BaseModel(ABC):
    def __init__(self, conf):
        self.config = Config.from_json(conf)

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass