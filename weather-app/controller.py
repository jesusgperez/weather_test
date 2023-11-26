import json
import requests
from flask import current_app
from typing import Dict, Tuple
from domain import TemperatureType
from config import API_URL, KELVIN_ZERO
from datetime import datetime, timedelta


def validate_arguments(query_params: Dict) -> Tuple[bool, str]:
    country, city = query_params.get('country'), query_params.get('city')

    if not country or not city:
        msg = 'Should send a country and city to make a request'
        return False, msg

    if not len(country) == 2:
        msg = 'Country should have only two chars'
        return False, msg

    return True, ''


def get_weather(query_params: Dict) -> Dict:
    cache = current_app.cache
    country, city = query_params['country'], query_params['city']
    country, city = country.lower(), city.lower()

    cached_response = cache.get(f'{country}_{city}')

    if cached_response:
        return serialize_data(api_data=cached_response)

    request_url = API_URL % (city, country)

    try:
        api_response = requests.get(request_url)
        api_response.raise_for_status()
    except Exception as e:
        msg = 'Unexpected error while fetching data'
        raise Exception(f'{msg}, error: ' + str(e))

    api_data = json.loads(api_response.content)

    cache.set(f'{country}_{city}', api_data)

    return serialize_data(api_data=api_data)


def serialize_data(api_data: Dict) -> Dict:
    city = api_data['name']
    country = api_data['sys']['country']
    temperature = api_data['main']['temp']
    pressure = api_data['main']['pressure']
    humidity = api_data['main']['humidity']
    sunrise = datetime.fromtimestamp(api_data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(api_data['sys']['sunset'])
    lat, lon = api_data['coord']['lat'], api_data['coord']['lon']

    response = {
        'location_name': f'{city}, {country}',
        'temperature': {
            'celcius': get_temperature(
                type=TemperatureType.CELSIUS,
                temperature=temperature
            ),
            'fahrenheit': get_temperature(
                type=TemperatureType.FAHRENHEIT,
                temperature=temperature
            )
        },
        'wind': api_data['wind'],
        'cloudness': api_data['weather'][0]['description'],
        'pressure': f'{pressure} hpa',
        'humidity': f'{humidity}%',
        'sunrise': '%02d:%02d' % (sunrise.hour, sunrise.minute),
        'sunset': '%02d:%02d' % (sunset.hour, sunset.minute),
        'coordinates': f'[{lat}, {lon}]',
        'requested_time': datetime.now() - timedelta(hours=5),
        'forecast': {}
    }

    return response


def get_temperature(type: TemperatureType, temperature: int) -> int:
    if type == TemperatureType.CELSIUS:
        return round(temperature - KELVIN_ZERO, 2)

    return round((temperature - KELVIN_ZERO)*9/5 + 32, 2)
