import logging
from flask_cors import CORS
from flask.json import jsonify
from flask_login import login_required, current_user
from flask import Blueprint, request, current_app
from goodtablesio import exceptions
from goodtablesio.models.job import Job
from goodtablesio.models.source import Source
from goodtablesio.tasks.validate import validate
from goodtablesio.utils.jobconf import verify_validation_conf
from goodtablesio.utils.backend import ApiError, token_required, list_endpoints
log = logging.getLogger(__name__)


# Create blueprint

api = Blueprint('api', __name__, url_prefix='/api')
CORS(api)


# General endpoints

@api.route('/')
@token_required
def help(user):
    return jsonify({
        'endpoints': list_endpoints(current_app, url_prefix='/api')
    })


@api.route('/source')
@token_required
def source_list(user):
    return jsonify({
        'sources': [source.to_api() for source in user.sources],
    })


@api.route('/source/<source_id>')
@token_required
def source_get(source_id, user):
    source = Source.get(source_id)
    if not source:
        raise ApiError(404, 'Not Found')
    if source not in user.sources:
        if source.conf.get('private'):
            raise ApiError(403, 'Forbidden')
    return jsonify({
        'source': source.to_api(),
    })


@api.route('/source', methods=['POST'])
@token_required
def source_create(user):
    data = request.get_json()
    name = data.get('name')
    private = data.get('private', False)
    if not name:
        raise ApiError(400, 'Source name is required')
    if Source.get_by_integration_and_name('api', name):
        raise ApiError(409, 'Source name is in use')
    source = Source.create(
        name=name,
        active=True,
        conf={'private': private},
        integration_name='api',
        users=[user],
    )
    return jsonify({
        'source': source.to_api(),
    })


@api.route('/source/<source_id>/job')
@token_required
def source_job_list(source_id, user):
    source = Source.get(source_id)
    if not source:
        raise ApiError(404, 'Not Found')
    if source not in user.sources:
        if source.conf.get('private'):
            raise ApiError(403, 'Forbidden')
    jobs = (Job.query().filter_by(source_id=source_id)
            .order_by(Job.created.desc()).limit(10).all())

    return jsonify({
        'jobs': [job.to_api() for job in jobs],
    })


@api.route('/source/<source_id>/job/<job_id>')
@token_required
def source_job_get(source_id, job_id, user):
    job = Job.query().filter_by(source_id=source_id, id=job_id).one_or_none()
    if not job:
        raise ApiError(404, 'Not Found')
    if job.source.conf.get('private'):
        if job.source not in user.sources:
            raise ApiError(403, 'Forbidden')
    return jsonify({
        'job': job.to_api(),
    })


@api.route('/source/<source_id>/job', methods=['POST'])
@token_required
def source_job_create(source_id, user):

    # Get source
    source = Source.get(source_id)
    if not source:
        raise ApiError(404, 'Not Found')
    if source not in user.sources:
        raise ApiError(403, 'Forbidden')
    if source.integration_name != 'api':
        raise ApiError(403, 'Forbidden')

    # Get validation configuration
    validation_conf = request.get_json()
    if not validation_conf:
        raise ApiError(400, 'Missing configuration')

    # Verify validation configuration
    try:
        verify_validation_conf(validation_conf)
    except exceptions.InvalidValidationConfiguration:
        raise ApiError(400, 'Invalid configuration')

    # Create and run job
    job = Job.create(source=source)
    validate.delay(validation_conf, job_id=job.id)

    return jsonify({
        'job': job.to_api(),
    })


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


# Blueprint service

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
