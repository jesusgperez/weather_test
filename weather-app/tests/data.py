test_serialize_dict = {
    "base": "stations",
    "clouds": {
        "all": 20
    },
    "cod": 200,
    "coord": {
        "lat": 4.6097,
        "lon": -74.0817
    },
    "dt": 1701014124,
    "id": 3688689,
    "main": {
        "feels_like": 291.06,
        "humidity": 48,
        "pressure": 1028,
        "temp": 291.88,
        "temp_max": 291.88,
        "temp_min": 291.88
    },
    "name": "Bogota",
    "sys": {
        "country": "CO",
        "id": 8582,
        "sunrise": 1700995635,
        "sunset": 1701038416,
        "type": 1
    },
    "timezone": -18000,
    "visibility": 10000,
    "weather": [
        {
            "description": "few clouds",
            "icon": "02d",
            "id": 801,
            "main": "Clouds"
        }
    ],
    "wind": {
        "deg": 140,
        "speed": 6.17
    }
}

SERIALIZE_REQUIRED_KEYS = [
    'cloudness',
    'coordinates',
    'forecast',
    'humidity',
    'location_name',
    'pressure',
    'requested_time',
    'sunrise',
    'sunset',
    'temperature',
    'wind'
]


SERIALIZED_DATA = {
    'location_name': 'Bogota, CO',
    'temperature': {'celcius': 565.03, 'fahrenheit': 1049.05},
    'wind': {'deg': 140, 'speed': 6.17},
    'cloudness': 'few clouds',
    'pressure': '1028 hpa',
    'humidity': '48%',
    'sunrise': '05:47',
    'sunset': '17:40',
    'coordinates': '[4.6097, -74.0817]',
    'forecast': {}
}
