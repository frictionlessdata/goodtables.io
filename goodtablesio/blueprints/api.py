import uuid
import logging
from flask import Blueprint, request
from flask.json import jsonify
from flask_login import login_required, current_user
from goodtablesio import models
from goodtablesio import exceptions
from goodtablesio.tasks.validate import validate
from goodtablesio.utils.jobconf import verify_validation_conf
from goodtablesio.utils.backend import ApiError, token_required
log = logging.getLogger(__name__)


# Create blueprint

api = Blueprint('api', __name__, url_prefix='/api')


# General endpoints

@api.route('/')
@token_required
def root(user):
    return jsonify({'help': 'todo'})


@api.route('/job/<job_id>')
@token_required
def job_get(job_id, user):
    job = models.job.get(job_id)
    if job:
        return jsonify(job)
    else:
        raise ApiError(404, 'Job not found')


@api.route('/job')
@token_required
def job_list(user):
    return jsonify(models.job.get_ids())


@api.route('/job', methods=['POST'])
@token_required
def job_create(user):

    # Get validation configuration
    validation_conf = request.get_json()
    if not validation_conf:
        raise ApiError(400, 'Missing configuration')

    # Validate validation configuration
    try:
        verify_validation_conf(validation_conf)
    except exceptions.InvalidValidationConfiguration:
        raise ApiError(400, 'Invalid configuration')

    # Create job
    job_id = str(uuid.uuid4())
    models.job.create({'id': job_id})

    # Create celery task
    validate.delay(validation_conf, job_id=job_id)

    return job_id


# Token endpoints

@api.route('/token')
@login_required
def token_list():
    return jsonify({
        'tokens': [token.to_api() for token in current_user.api_tokens],
    })


@api.route('/token', methods=['POST'])
@login_required
def token_create():
    data = request.get_json()
    token = current_user.create_api_token(description=data.get('description'))
    return jsonify({
        'token': token.to_api(),
    })


@api.route('/token/<token_id>', methods=['DELETE'])
@login_required
def token_delete(token_id):
    success = current_user.delete_api_token(token_id)
    if not success:
        raise ApiError(404, 'Token not found')
    return jsonify({
        'token_id': token_id,
    })


# Service functions

@api.app_errorhandler(Exception)
def handle_api_errors(error):
    # TODO: this is not really correct way to catch blueprint errors
    # because flask doesn't support error handlers per blueprint
    # so this error handler is global for the whole app
    if api.debug:
        raise error
    if not isinstance(error, ApiError):
        log.exception(repr(error))
    message = getattr(error, 'message', 'Internal Error')
    status_code = getattr(error, 'status_code', 500)
    response = jsonify({'message': message})
    response.status_code = status_code
    return response


@api.record
def record_params(setup_state):
    api.debug = setup_state.app.debug
