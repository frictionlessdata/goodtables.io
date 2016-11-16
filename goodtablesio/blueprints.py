from flask import Blueprint, request, abort
from flask.json import jsonify
from goodtablesio import exceptions
from goodtablesio import helpers


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/job', methods=['POST'])
def create_job():

    # Get validation configuration
    validation_conf = request.get_json()
    if not validation_conf:
        abort(400, 'Missing configuration')

    # Create job
    try:
        job_id = helpers.create_job(validation_conf)
    except exceptions.InvalidValidationConfiguration:
        abort(400, 'Invalid configuration')

    return job_id


@api.route('/job')
def list_jobs():
    return jsonify(helpers.get_job_ids())


@api.route('/job/<job_id>')
def get_job(job_id):
    return jsonify(helpers.get_job(job_id))


@api.route('/')
def hi():
    return "hi"
