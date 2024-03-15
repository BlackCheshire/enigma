from Crypto.Hash import SHA512


def calc_hash(data: bytes) -> bytes:
    sha = SHA512.new()
    sha.update(data)
    digest = sha.digest()
    hash = digest[:20]
    return hash
