from dataclasses import dataclass, field

from .keys import RsaKeys
from ..core.signers.pkcs1_pss import PKCS1Signer


@dataclass(frozen=True)
class RSASigner:
    passphrase: str = field(repr=False, default=None)

    def __call__(self, keys: RsaKeys) -> bytes:
        signer = PKCS1Signer(secret=self.passphrase)
        private_key = keys.value_dict['privKey']
        return signer.sign_digest(private_key=private_key)


@dataclass(frozen=True)
class RSAVerifier:
    passphrase: str = field(repr=False, default=None)
    signature: bytes = field(repr=False, default=None)

    def __call__(self, keys: RsaKeys) -> bool:
        verifier = PKCS1Signer(secret=self.passphrase)
        public_key = keys.value_dict['pubKey']
        return verifier.verify_digest(signature=self.signature, public_key=public_key)
