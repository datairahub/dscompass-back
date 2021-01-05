from dataclasses import dataclass, field
from typing import Tuple

from .keys import RsaKeys
from ..core.base_cipher import BaseCipher
from ..core.ciphers.pkcs10_oaep import PKCS1OAEPBaseCipher


@dataclass
class RSAData:
    cipher: BaseCipher = field(repr=False, default=None)
    data: Tuple[str, bytes] = field(repr=False, default=tuple())

    def encrypt(self, value: bytes):
        self.data = self.cipher.encrypt_and_sign(plain_text=value)
        return self

    def decrypt(self, signature: bytes, value: bytes):
        self.data = self.cipher.decrypt_and_verify(cipher_text=value, signature=signature)
        return self


@dataclass(frozen=True)
class RSADataCrypt:
    passphrase: str = field(repr=False, default=None)
    secret_signer: str = field(repr=False, default=None)

    def __call__(self, value: bytes, keys: RsaKeys) -> RSAData:
        private_key = keys.value_dict['privKey']
        public_key = keys.value_dict['privKey']
        cipher = PKCS1OAEPBaseCipher(secret_cipher=self.passphrase, secret_signer=self.secret_signer,
                                     private_key=private_key, public_key=public_key)
        data_cipher = RSAData(cipher=cipher).encrypt(value=value)
        return data_cipher


@dataclass(frozen=True)
class RSADataDecrypt:
    passphrase: str = field(repr=False, default=None)
    secret_signer: str = field(repr=False, default=None)

    def __call__(self, value: bytes, signature: bytes, keys: RsaKeys) -> RSAData:
        private_key = keys.value_dict['privKey']
        public_key = keys.value_dict['privKey']
        cipher = PKCS1OAEPBaseCipher(secret_cipher=self.passphrase, secret_signer=self.secret_signer,
                                     private_key=private_key, public_key=public_key)
        data_cipher = RSAData(cipher=cipher).decrypt(value=value, signature=signature)
        return data_cipher
