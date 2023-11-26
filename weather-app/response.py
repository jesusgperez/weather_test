from flask import jsonify
from typing import Tuple, Any, Dict
from werkzeug.http import HTTP_STATUS_CODES


def error_response(
    status_code: int,
    message: str = None
) -> Tuple[str, int]:
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    return response, status_code


def bad_request(message: str) -> Tuple[str, int]:
    return error_response(message=message, status_code=400)


def success_request(message: Dict[Any, Any]) -> Tuple[str, int]:
    response = jsonify(message)
    return response, 200
