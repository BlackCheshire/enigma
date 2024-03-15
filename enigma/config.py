from typing import NamedTuple
from typing import NoReturn
import os

from dotenv import load_dotenv

from enigma.log import log
from os import environ


class Config(NamedTuple):
    app_host: str
    app_port: int
    app_log_level: str
    redis_host: str
    redis_port: int
    redis_username: str
    redis_password: str
    encrypt_key: bytes
    encrypt_cache_prefix: str
    encrypt_cache_ttl: int


def get_config() -> Config:
    global _config
    if _config is None:
        _config = _init_config()
    return _config


# Private


_config: Config | None = None


def _init_config() -> Config:
    log.info('Initializing config')
    load_dotenv()
    config = Config(
        app_host=os.getenv('APP_HOST'),
        app_port=int(os.getenv('APP_PORT')),
        app_log_level=os.getenv('APP_LOG_LEVEL'),
        redis_host=os.getenv('REDIS_HOST'),
        redis_port=int(os.getenv('REDIS_PORT')),
        redis_username=os.getenv('REDIS_USERNAME'),
        redis_password=os.getenv('REDIS_PASSWORD'),
        encrypt_key=os.getenvb('ENCRYPT_KEY'),
        encrypt_cache_prefix=os.getenv('ENCRYPT_CACHE_PREFIX'),
        encrypt_cache_ttl=int(os.getenv('ENCRYPT_CACHE_TTL')),
    )
    log.info('Config initialized')
    return config


def _get_env_str(key: str) -> str:
    try:
        str_value = os.environ[key]
    except KeyError:
        _error(f'No value configured for key "{key}"')
    return str_value


def _get_env_int(key: str) -> int:
    str_value = _get_env_str(key)
    try:
        int_value = int(str_value)
    except ValueError:
        _error(f'Invalid int value "{str_value}" for key "{key}"')
    return int_value


def _get_env_bytes(key: str) -> bytes:
    str_value = _get_env_str(key)
    try:
        bytes_value = bytes.fromhex(str_value)
    except ValueError:
        _error(f'Invalid hex bytes value "{str_value}" for key "{key}"')
    return bytes_value


def _error(msg: str) -> NoReturn:
    log.error(f'Config init error: {msg}')
    raise Exception(msg)
