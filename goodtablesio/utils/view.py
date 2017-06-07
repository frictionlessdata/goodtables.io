import datetime
from flask import make_response
from werkzeug.http import http_date
from functools import wraps, update_wrapper


# Module API

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
