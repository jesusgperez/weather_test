from typing import Dict
from domain import TemperatureType
from datetime import datetime, timedelta


def serialize_data(api_data: Dict) -> Dict:
    data = api_data['data']

    city = data['name']
    country = data['sys']['country']
    temperature = data['main']['temp']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(data['sys']['sunset'])
    lat, lon = data['coord']['lat'], data['coord']['lon']

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
        'wind': data['wind'],
        'cloudness': data['weather'][0]['description'],
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
