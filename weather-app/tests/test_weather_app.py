import json
from faker import Faker
from random import randint
from requests import Response
from unittest import TestCase
from unittest.mock import patch, Mock
from config import KELVIN_ZERO
from domain import TemperatureType
from controller import (
    validate_arguments,
    get_temperature,
    serialize_data,
    get_weather
)
from tests.data import (
    test_serialize_dict,
    SERIALIZE_REQUIRED_KEYS,
    SERIALIZED_DATA
)
from app import app

faker = Faker()


class TestWeatherApp(TestCase):
    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test__validate_arguments__failed(self):
        country = faker.country()

        valid, msg = validate_arguments(
            query_params={'country': country}
        )

        self.assertFalse(valid)
        self.assertEqual(
            msg,
            'Should send a country and city to make a request'
        )

        city = faker.city()

        valid, msg = validate_arguments(
            query_params={'city': city}
        )

        self.assertFalse(valid)
        self.assertEqual(
            msg,
            'Should send a country and city to make a request'
        )

        valid, msg = validate_arguments(
            query_params={'country': country, 'city': city}
        )

        self.assertFalse(valid)
        self.assertEqual(
            msg,
            'Country should have only two chars'
        )

    def test__serialize_data__success(self):
        data = serialize_data(api_data=test_serialize_dict)

        self.assertEqual(
            list(data.keys()).sort(),
            SERIALIZE_REQUIRED_KEYS.sort()
        )

    def test__get_temperature__success(self):
        kelvin_temp = randint(0, 300)
        celsius = round(kelvin_temp - KELVIN_ZERO, 2)
        fahrenheit = round(celsius*9/5 + 32, 2)

        self.assertEqual(
            get_temperature(
                type=TemperatureType.CELSIUS,
                temperature=kelvin_temp
            ),
            celsius
        )

        self.assertEqual(
            get_temperature(
                type=TemperatureType.FAHRENHEIT,
                temperature=kelvin_temp
            ),
            fahrenheit
        )

    @patch('controller.API_URL')
    @patch('controller.requests')
    @patch('controller.current_app')
    def test__get_weather__no_cache(
        self,
        mock_current_app,
        mock_requests,
        mock_api_url
    ):
        mock_cache = Mock()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        mock_current_app.cache = mock_cache

        content = json.dumps(test_serialize_dict)
        response = Response()
        response._content = content.encode()
        response.status_code = 200

        mock_requests.get.return_value = response

        country, city = faker.country().lower(), faker.city().lower()

        data = get_weather(
            query_params={'country': country, 'city': city}
        )

        del data['requested_time']

        self.assertTrue(data, SERIALIZED_DATA)
        mock_cache.set.assert_called_with(
            f'{country}_{city}',
            test_serialize_dict
        )

    @patch('controller.API_URL')
    @patch('controller.requests')
    @patch('controller.current_app')
    def test__get_weather__cache(
        self,
        mock_current_app,
        mock_requests,
        mock_api_url
    ):
        mock_cache = Mock()
        mock_cache.get.return_value = test_serialize_dict
        mock_current_app.cache = mock_cache

        content = json.dumps(test_serialize_dict)
        response = Response()
        response._content = content.encode()
        response.status_code = 200

        mock_requests.get.return_value = response

        country, city = faker.country(), faker.city()

        data = get_weather(
            query_params={'country': country, 'city': city}
        )

        del data['requested_time']

        self.assertTrue(data, SERIALIZED_DATA)

    @patch('controller.API_URL')
    @patch('controller.requests')
    @patch('controller.current_app')
    def test__get_weather__failed(
        self,
        mock_current_app,
        mock_requests,
        mock_api_url
    ):
        mock_cache = Mock()
        mock_cache.get.return_value = None
        mock_current_app.cache = mock_cache

        content = '400 Client Error: None for url: None'
        response = Response()
        response._content = content.encode()
        response.status_code = 400

        mock_requests.get.return_value = response

        country, city = faker.country(), faker.city()

        with self.assertRaises(Exception) as context:
            _ = get_weather(
                query_params={'country': country, 'city': city}
            )

        self.assertEqual(
            str(context.exception),
            f'Unexpected error while fetching data, error: {content}'
        )
