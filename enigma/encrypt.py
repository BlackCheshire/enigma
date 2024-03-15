from Crypto.Cipher import AES

from enigma.config import get_config
from enigma.hash import calc_hash


def encrypt_data(data: bytes) -> bytes:
    cfg = get_config()
    aes = AES.new(cfg.encrypt_key, AES.MODE_CBC)

    pad_bytes_len = _cbc_pad_bytes_len(len(data))
    if pad_bytes_len:
        data = data + b'\0' * pad_bytes_len

    encrypted_data = aes.encrypt(data)
    if pad_bytes_len:
        encrypted_data = encrypted_data[:-pad_bytes_len]

    return encrypted_data


def get_encrypt_key_fingerprint() -> bytes:
    global _key_fingerprint
    if _key_fingerprint is None:
        _key_fingerprint = _calc_key_fingerprint();
    return _key_fingerprint


# Private


_CBC_BLOCK_SIZE = 16


_key_fingerprint: bytes | None = None


def _calc_key_fingerprint() -> bytes:
    cfg = get_config()
    fingerprint = calc_hash(cfg.encrypt_key)
    return fingerprint


def _cbc_pad_bytes_len(data_len: int) -> int:
    if data_len % _CBC_BLOCK_SIZE == 0:
        return 0

    rem_len = data_len % _CBC_BLOCK_SIZE
    pad_len = _CBC_BLOCK_SIZE - rem_len
    return pad_len
