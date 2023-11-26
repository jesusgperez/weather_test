from requests import HTTPError
from flask import request, Blueprint
from response import bad_request, success_request
from controller import (
    get_weather,
    validate_arguments
)

weather = Blueprint('weather', __name__)

@weather.route('/')
def main():
    return {'hello': 'world'}


@weather.route('/weather', methods=['GET'])
def weather_service():
    valid, msg = validate_arguments(query_params=request.args)

    if not valid:
        return bad_request(message=msg)

    try:
        response = get_weather(query_params=request.args)
    except HTTPError as e:
        return bad_request(message=str(e))

    return success_request(
        message=response
    )