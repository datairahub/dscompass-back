from abc import abstractmethod, ABCMeta


class BaseSigner(metaclass=ABCMeta):
    @abstractmethod
    def sign_digest(self, *args, **kwargs):
        ...

    @abstractmethod
    def verify_digest(self, *args, **kwargs):
        ...
