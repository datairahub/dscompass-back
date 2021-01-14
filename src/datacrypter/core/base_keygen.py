from abc import abstractmethod, ABCMeta


class BaseKeyGen(metaclass=ABCMeta):
    @abstractmethod
    def generate_keys(self, *args, **kwargs):
        ...


class BaseKeyLoader(metaclass=ABCMeta):
    @abstractmethod
    def load_keys(self, *args, **kwargs):
        ...
