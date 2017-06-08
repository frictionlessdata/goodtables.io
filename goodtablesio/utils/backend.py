# pylama:ignore=E301
import datetime
from werkzeug.http import http_date
from flask import make_response, request, url_for
from functools import wraps, update_wrapper
from goodtablesio.models.user import User


# Module API

def list_endpoints(app, url_prefix=''):
    endpoints = []
    for rule in app.url_map.iter_rules():
        url = rule.rule
        methods = ','.join(rule.methods)
        if not url.startswith(url_prefix):
            continue
        endpoints.append({
            'url': url,
            'methods': methods,
        })
    return endpoints


def no_cache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        http_now = http_date(datetime.datetime.now())
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = http_now
        response.headers['Expires'] = http_now
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Pragma'] = 'no-cache'
        return response
    return update_wrapper(no_cache, view)


def token_required(view):
    @wraps(view)
    def decorated_view(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            raise ApiError(401, 'Unauthorized')
        user = User.get_by_api_token(token)
        if not user:
            raise ApiError(401, 'Unauthorized')
        return view(*args, user=user, **kwargs)
    return decorated_view


class ApiError(Exception):
    status_code = 400
    def __init__(self, status_code, message):
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message
