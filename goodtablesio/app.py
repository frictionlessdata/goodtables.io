from flask import Flask, render_template
from .blueprints.api import api
from .blueprints.site import site
from .plugins.github.blueprint import github


# Module API

# Create instance
app = Flask(__name__)

app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(site)

# Register plugins
app.register_blueprint(github)


# Set error handlers

@app.errorhandler(404)
def not_found_error(err):
    return (render_template('error404.html'), 404)


@app.errorhandler(500)
def server_error(err):
    return (render_template('error500.html'), 500)
