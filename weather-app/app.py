from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': 'rediss://127.0.0.1:6379'})

@app.route('/')
def main():
    return {'hello': 'world'}
