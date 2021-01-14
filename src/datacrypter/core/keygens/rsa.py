
from Crypto.PublicKey.RSA import RsaKey, import_key
from Crypto.PublicKey.RSA import generate as crypto_generator
from ..base_keygen import BaseKeyGen, BaseKeyLoader


class RSAKeyLoader(BaseKeyLoader):
    @staticmethod
    def load_keys(extern_key: str or bytes, passphrase: str) -> RsaKey:
        return import_key(extern_key=extern_key, passphrase=passphrase)


class RSAKeyGen(BaseKeyGen):
    def __init__(self, crypto_key: RsaKey = None, key_size: int = None, pk_cs: int = None, protection: str = None):
        self.crypto_key = crypto_key or crypto_generator
        self.key_size = key_size or 2048
        self._pub_key_crypto_standard = pk_cs or 8
        self._protection = protection or "scryptAndAES256-CBC"

    def generate_keys(self) -> RsaKey:
        keys = self.crypto_key(bits=self.key_size)
        return keys

    def get_private_key(self, keys: RsaKey, passphrase: str) -> str:
        private_key = keys.exportKey(passphrase=passphrase, pkcs=self._pub_key_crypto_standard,
                                     protection=self._protection)
        return private_key.decode()

    @staticmethod
    def get_public_key(keys: RsaKey) -> str:
        public_key = keys.publickey().exportKey()
        return public_key.decode()
