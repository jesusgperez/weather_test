from flask import Flask, request
from flask_caching import Cache
from config import *

app = Flask(__name__)
cache = Cache(app, config=CACHE_CONFIG)

@app.route('/')
def main():
    return {'hello': 'world'}

@app.route('/weather', methods=['GET', 'POST'])
def weather_service():
    if request.method == 'GET':
        return {
            'country': cache.get('country'),
            'city': cache.get('city')
        }

    args = request.args

    country, city = args.get('country'), args.get('city')

    if not country or not city:
        return 'incorrent args'

    cache.set('country', country, timeout=10)
    cache.set('city', city, timeout=10)

    return 'this is a post request'