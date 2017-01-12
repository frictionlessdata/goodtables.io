import logging
import uuid

from flask import Blueprint, request
from flask.json import jsonify

from goodtablesio import exceptions
from goodtablesio import models
from goodtablesio import tasks
from goodtablesio.utils.jobconf import verify_validation_conf

log = logging.getLogger(__name__)


# Module API

api = Blueprint('api', __name__, url_prefix='/api')


class APIError(Exception):
    status_code = 400

    def __init__(self, status_code, message):
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message


@api.record
def record_params(setup_state):
    api.debug = setup_state.app.debug


@api.app_errorhandler(Exception)
def handle_api_errors(error):
    # TODO: this is not really correct way to catch blueprint errors
    # because flask doesn't support error handlers per blueprint
    # so this error handler is global for the whole app
    if api.debug:
        raise error
    if not isinstance(error, APIError):
        log.exception(repr(error))
    message = getattr(error, 'message', 'Internal Error')
    status_code = getattr(error, 'status_code', 500)
    response = jsonify({'message': message})
    response.status_code = status_code
    return response


@api.route('/')
def root():
    return jsonify({'help': 'todo'})


@api.route('/job', methods=['POST'])
def create_job():

    # Get validation configuration
    validation_conf = request.get_json()
    if not validation_conf:
        raise APIError(400, 'Missing configuration')

    # Validate validation configuration

    try:
        verify_validation_conf(validation_conf)
    except exceptions.InvalidValidationConfiguration:
        raise APIError(400, 'Invalid configuration')

    job_id = str(uuid.uuid4())

    # Write to database
    models.job.create({'id': job_id})

    # Create celery task
    tasks.validate.delay(validation_conf, job_id=job_id)

    return job_id


@api.route('/job')
def list_jobs():
    return jsonify(models.job.get_ids())


@api.route('/job/<job_id>')
def get_job(job_id):
    job = models.job.get(job_id)
    if job:
        return jsonify(job)
    else:
        raise APIError(404, 'Job not found')
