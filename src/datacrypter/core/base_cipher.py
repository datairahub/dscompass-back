from abc import abstractmethod, ABCMeta


class BaseCipher(metaclass=ABCMeta):
    @abstractmethod
    def _get_cipher(self, *args, **kwargs):
        ...

    @abstractmethod
    def encrypt_and_sign(self, *args, **kwargs):
        ...

    @abstractmethod
    def decrypt_and_verify(self, *args, **kwargs):
        ...
