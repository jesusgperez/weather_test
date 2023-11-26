from config import *
from flask_caching import Cache
from flask import Flask, request
from response import bad_request, success_request
from controller import (
    get_weather,
    validate_arguments
)

app = Flask(__name__)
cache = Cache(app, config=CACHE_CONFIG)


@app.route('/')
def main():
    return {'hello': 'world'}


@app.route('/weather', methods=['GET'])
def weather_service():
    valid, msg = validate_arguments(query_params=request.args)

    if not valid:
        return bad_request(message=msg)

    return success_request(
        message=get_weather(query_params=request.args)
    )
