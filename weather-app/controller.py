from typing import Dict
from domain import TemperatureType
from datetime import datetime, timedelta


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
        return round(temperature - 273.15, 2)

    return round((temperature - 273.15)*9/5 + 32, 2)
