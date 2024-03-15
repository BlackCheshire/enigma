from base64 import b64encode

from fastapi import APIRouter
from fastapi import Request

from enigma.cache import get_cache_value
from enigma.cache import set_cache_value
from enigma.config import get_config
from enigma.encrypt import encrypt_data
from enigma.encrypt import get_encrypt_key_fingerprint
from enigma.hash import calc_hash
from enigma.log import log
from enigma.model import EncryptRequest
from enigma.model import EncryptResponse
from enigma.request import gen_request_id


router = APIRouter(prefix='/api/encrypt')


@router.post('')
async def post_encrypt(request: EncryptRequest, r: Request) -> EncryptResponse:
    request_id = gen_request_id()
    log.debug(f'Request {request_id} from {r.client.host}:{r.client.port} in processing')

    key_fingerprint = get_encrypt_key_fingerprint()
    key_fingerprint_hex = key_fingerprint.hex()
    log.debug(f'Request {request_id} key fingerpint is "{key_fingerprint_hex}"')

    data_hash = calc_hash(request.data)
    data_hash_hex = data_hash.hex()
    log.debug(f'Request {request_id} data hash is "{data_hash_hex}"')

    cfg = get_config()
    cache_key = f'{cfg.encrypt_cache_prefix}:{key_fingerprint_hex}:{data_hash_hex}'
    log.debug(f'Request {request_id} cache key is "{cache_key}"')
    encrypted_data = await get_cache_value(cache_key)
    if encrypted_data is None:
        log.debug(f'Request {request_id} has no encrypted data in cache to use')
        encrypted_data = encrypt_data(request.data)
        log.debug(f'Request {request_id} encrypted its data')
        await set_cache_value(cache_key, encrypted_data, cfg.encrypt_cache_ttl)
        log.debug(f'Request {request_id} cached its encrypted data')
    else:
        log.debug(f'Request {request_id} used ecrypted data from cache')

    response = EncryptResponse.model_construct(
        data_hash=b64encode(data_hash).decode(),
        encrypted_data=b64encode(encrypted_data).decode(),
        key_fingerprint=b64encode(key_fingerprint).decode(),
    )
    log.debug(f'Request {request_id} processed successfully')
    return response
