from dataclasses import dataclass, field
from typing import Dict, Any

from ..core.keygens.rsa import RSAKeyGen


@dataclass(frozen=True)
class RsaKeys:
    value_dict: Dict[Any, str] = field(repr=False, default=None)


@dataclass(frozen=True)
class RSAKeysGenerator:
    passphrase: str = field(repr=False, default=None)

    def __call__(self, key_gen: RSAKeyGen = None) -> RsaKeys:
        if key_gen is None:
            key_gen = RSAKeyGen()
        keys = key_gen.generate_keys()
        private_key = key_gen.get_private_key(keys=keys, passphrase=self.passphrase)
        public_key = key_gen.get_public_key(keys=keys)
        return RsaKeys(value_dict=dict(privKey=private_key, pubKey=public_key))
