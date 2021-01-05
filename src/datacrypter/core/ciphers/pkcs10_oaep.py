from base64 import b64encode, b64decode
from typing import Tuple, List

from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher
from Crypto.Cipher.PKCS1_OAEP import new as pkcs1_oaep_new
from Crypto.Hash import SHA3_256
from Crypto.Hash.SHA3_256 import SHA3_256_Hash
from Crypto.Util.number import ceil_div
from Crypto.Util.number import size as n_size

from ..base_cipher import BaseCipher
from ..base_keygen import BaseKeyLoader
from ..keygens.rsa import RSAKeyLoader
from ..signers.pkcs1_pss import PKCS1Signer


class PKCS1OAEPBaseCipher(BaseCipher):
    def __init__(self, keys_loader: BaseKeyLoader = None, hash_module: SHA3_256_Hash = None, secret_cipher: str = None,
                 secret_signer: str = None, private_key: str or bytes = None, public_key: str or bytes = None):
        self._rsa_keys_loader = keys_loader or RSAKeyLoader()
        self._hash = hash_module or SHA3_256
        self._secret = secret_cipher
        self._secret_signer = secret_signer
        self._priv_key = private_key
        self._pub_key = public_key

    def _get_cipher(self, key: str or bytes, hash_module) -> PKCS1OAEP_Cipher:
        return pkcs1_oaep_new(key=key, hashAlgo=hash_module)

    def _load_keys(self, key):
        imported_key = self._rsa_keys_loader.load_keys(extern_key=key, passphrase=self._secret)
        return imported_key

    def _load_cipher_with_keys(self, key: str or bytes = None) -> PKCS1OAEP_Cipher:
        imported_key = self._load_keys(key=key)
        cipher = self._get_cipher(key=imported_key, hash_module=self._hash)
        return cipher

    @staticmethod
    def _chunk_size(cipher: PKCS1OAEP_Cipher) -> int:
        key_n_in_bits = n_size(N=cipher._key.n)
        key_length = ceil_div(key_n_in_bits, 8)
        hash_length = cipher._hashObj.digest_size * 2

        max_chunk_size = key_length - hash_length - 2

        return max_chunk_size

    @staticmethod
    def _split_value_to_encrypt(plain_text: bytes = None, max_size: int = None) -> List[bytes]:
        range_start, range_stop, range_step = 0, len(plain_text), max_size
        chunked_text = [plain_text[i:i + max_size] for i in range(range_start, range_stop, range_step)]

        return chunked_text

    def encrypt_and_sign(self, plain_text: bytes = None) -> Tuple[str, bytes]:
        cipher = self._load_cipher_with_keys(key=self._pub_key)
        size = self._chunk_size(cipher=cipher)
        chunked_text_values = self._split_value_to_encrypt(plain_text=plain_text, max_size=size)
        encrypted_text = ','.join(b64encode(cipher.encrypt(message=value)).decode() for value in chunked_text_values)

        signer = PKCS1Signer(secret=self._secret_signer)
        signature = signer.sign_digest(private_key=self._priv_key)

        return encrypted_text, signature

    def decrypt_and_verify(self, cipher_text: bytes = None, signature: bytes = None) -> str:
        cipher = self._load_cipher_with_keys(key=self._priv_key)
        cipher_text_values = cipher_text.decode().split(',')
        decrypted_text_values = [cipher.decrypt(ciphertext=b64decode(text)) for text in cipher_text_values]
        decrypted_text = ''.join([value.decode() for value in decrypted_text_values])

        verifier = PKCS1Signer(secret=self._secret_signer)
        is_verified = verifier.verify_digest(public_key=self._pub_key, signature=signature)
        if is_verified is True:
            return decrypted_text
        return ''
