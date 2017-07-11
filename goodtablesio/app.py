import os
from urllib.parse import urlparse
import logging

import sqlalchemy
from flask import Flask, request, jsonify
from raven.contrib.flask import Sentry

from goodtablesio import settings
from goodtablesio.auth import oauth, login_manager
from goodtablesio.blueprints.api import api
from goodtablesio.blueprints.site import site
from goodtablesio.blueprints.user import user
from goodtablesio.integrations.github.blueprint import github
from goodtablesio.integrations.s3.blueprint import s3
from goodtablesio.utils.frontend import render_component
from goodtablesio.services import database
log = logging.getLogger(__name__)


# Module API

# Create instance
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'public'),
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'public')
)
app.secret_key = settings.FLASK_SECRET_KEY

url_parts = urlparse(settings.BASE_URL)
app.config['SERVER_NAME'] = url_parts.netloc
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.config['MAX_CONTENT_LENGTH'] = settings.FLASK_MAX_CONTENT_LENGTH

# Register Flask integrations
oauth.init_app(app)
login_manager.init_app(app)
if settings.SENTRY_DSN:
    Sentry(app, dsn=settings.SENTRY_DSN)

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(site)
app.register_blueprint(user)

# Register integrations
app.register_blueprint(github)
app.register_blueprint(s3)


# Set error handlers
@app.errorhandler(401)
def not_authorized_error(err):
    return _error_response(401, err)


@app.errorhandler(404)
def not_found_error(err):
    return _error_response(404, err)


@app.errorhandler(500)
def server_error(err):
    return _error_response(500, err)


@app.errorhandler(sqlalchemy.exc.SQLAlchemyError)
def error_handler(err):
    # To prevent session from break because of unhandled error with no rollback
    # https://github.com/frictionlessdata/goodtables.io/issues/97
    log.info('Database session rollback by server error handler')
    database['session'].rollback()
    raise err


def _error_response(code, err):
    if request.path.startswith('/api/'):
        return jsonify({
            'status': code,
            'message': err.description}), code
    else:
        return (render_component('Error{}'.format(code),
                                 props={'message': err.description}),
                code)
