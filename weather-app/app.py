import json
import requests
from config import *
from flask_caching import Cache
from flask import Flask, request
from response import bad_request, success_request
from controller import serialize_data

app = Flask(__name__)
cache = Cache(app, config=CACHE_CONFIG)

@app.route('/')
def main():
    return {'hello': 'world'}

@app.route('/weather', methods=['GET'])
def weather_service():
    args = request.args
    country, city = args.get('country'), args.get('city')

    if not country or not city:
        msg = 'Should send a country and city to make a request'
        return bad_request(message=msg)

    if not len(country) == 2:
        msg = 'Country should have only two chars'
        return bad_request(message=msg)

    country, city = country.lower(), city.lower()

    cached_response = {'data': cache.get(f'{country}_{city}')}

    if cached_response['data']:
        response = serialize_data(api_data=cached_response)
        return success_request(response)

    request_url = API_URL % (city, country)

    api_response = requests.get(request_url)
    api_data = json.loads(api_response.content)

    cache.set(f'{country}_{city}', api_data)

    response = serialize_data(api_data={'data': api_data})
    return success_request(message=response)
