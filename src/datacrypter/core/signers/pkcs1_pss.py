from base64 import b64encode, b64decode

from Crypto.Hash.SHA3_256 import SHA3_256_Hash
from Crypto.Hash.SHA3_256 import new as new_sha3_256
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pss
from Crypto.Signature.pss import PSS_SigScheme

from ..base_keygen import BaseKeyLoader
from ..base_signer import BaseSigner
from ..keygens.rsa import RSAKeyLoader


class PKCS1Signer(BaseSigner):
    def __init__(self, keys_loader: BaseKeyLoader = None, digest: SHA3_256_Hash = None, secret: str = None):
        self._rsa_keys_loader = keys_loader or RSAKeyLoader()
        self._digest = digest or new_sha3_256
        self._secret = secret or ''

    def digest(self, secret: bytes) -> SHA3_256_Hash:
        self._digest = self._digest().update(secret)
        return self._digest

    def _load_keys(self, key):
        imported_key = self._rsa_keys_loader.load_keys(extern_key=key, passphrase=self._secret)
        return imported_key

    def _get_signer(self, key: RsaKey) -> PSS_SigScheme:
        self._digest = self.digest(secret=self._secret.encode())
        signer = pss.new(rsa_key=key)

        return signer

    def sign_digest(self, private_key: str or bytes) -> bytes:
        imported_key = self._load_keys(key=private_key)
        signer = self._get_signer(key=imported_key)
        signature = signer.sign(msg_hash=self._digest)
        return b64encode(signature)

    def verify_digest(self, signature: bytes, public_key: str or bytes) -> bool:
        imported_key = self._load_keys(key=public_key)
        verifier = self._get_signer(key=imported_key)
        decoded_signature = b64decode(signature)
        try:
            verifier.verify(msg_hash=self._digest, signature=decoded_signature)
            return True
        except (ValueError, TypeError):
            return False
