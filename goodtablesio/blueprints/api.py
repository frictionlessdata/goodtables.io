from flask import Blueprint, request
from flask.json import jsonify

from goodtablesio import exceptions
from goodtablesio import helpers


# Module API

api = Blueprint('api', __name__, url_prefix='/api')


class APIError(Exception):
    status_code = 400

    def __init__(self, status_code, message):
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message

    def to_dict(self):
        return {'message': self.message}


@api.app_errorhandler(APIError)
def handle_api_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
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

    # Create job
    try:
        job_id = helpers.create_job(validation_conf)
    except exceptions.InvalidValidationConfiguration:
        raise APIError(400, 'Invalid configuration')

    return job_id


@api.route('/job')
def list_jobs():
    return jsonify(helpers.get_job_ids())


@api.route('/job/<job_id>')
def get_job(job_id):
    job = helpers.get_job(job_id)
    if job:
        return jsonify(job)
    else:
        raise APIError(404, 'Job Not Found')
