from pydantic import Base64Bytes
from pydantic import BaseModel


class EncryptRequest(BaseModel):
    data: Base64Bytes


class EncryptResponse(BaseModel):
    data_hash: str
    encrypted_data: str
    key_fingerprint: str
