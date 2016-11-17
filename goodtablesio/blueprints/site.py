from flask import Blueprint, request, abort, render_template
from flask.json import jsonify
from goodtablesio import exceptions
from goodtablesio import helpers


# Module API

site = Blueprint('site', __name__)


@site.route('/')
def home():
    return 'goodtables.io'


@site.route('/report/<job_id>')
def report(job_id):
    job = helpers.get_job(job_id)
    return render_template('report.html', job=job)
