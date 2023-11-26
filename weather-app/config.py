import os

CACHE_CONFIG = {
    'CACHE_TYPE': os.environ.get('CACHE_TYPE'),
    'CACHE_REDIS_URL': os.environ.get('CACHE_REDIS_URL'),
    'CACHE_DEFAULT_TIMEOUT': os.environ.get('CACHE_DEFAULT_TIMEOUT')
}

API_URL = os.environ.get('API_URL')
KELVIN_ZERO = -273.15
