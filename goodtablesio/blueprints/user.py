import logging
from urllib.parse import urlparse

from flask import Blueprint, request, session, redirect, url_for, abort, flash
from flask_login import login_user, logout_user, login_required, current_user

from goodtablesio import settings
from goodtablesio.services import database
from goodtablesio.models.user import User
from goodtablesio.auth import github_auth
from goodtablesio.utils.frontend import render_component

log = logging.getLogger(__name__)

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@login_required
def home():
    return render_component('User', props={
        'userName': getattr(current_user, 'display_name', None),
        'userEmail': getattr(current_user, 'email', None),
    })


@user.route('/login/<any(github):provider>')
def login(provider):
    if current_user.is_authenticated:
        flash('You are already logged in. Please log out if you want to ' +
              'log in with a different account', 'warning')
        return redirect(url_for('site.home'))

    # TODO: redirect to "next"
    url_parts = urlparse(settings.BASE_URL)
    callback_url = url_for('user.authorized', provider=provider,
                           _external=True, _scheme=url_parts.scheme)
    if provider == 'github':
        return github_auth.authorize(callback=callback_url)


@user.route('/logout')
def logout():

    # Clear user session
    session.clear()

    # Logout user with Flask-Login
    logout_user()

    return redirect(url_for('site.home'))


def _get_user_by_provider_id(provider_name, provider_id):
    return database['session'].query(User).filter(
        User.provider_ids[provider_name].astext == str(provider_id)
        ).one_or_none()


def _get_user_by_email(email):
    return database['session'].query(User).filter_by(
        email=email).one_or_none()


@user.route('/login/<any(github):provider>/authorized')
def authorized(provider):

    if provider == 'github':
        response = github_auth.authorized_response()
        if response is None or response.get('access_token') is None:
            # TODO: what to show to users?
            log.warning('Access denied: {0}, {1}, {2}'.format(
                request.args['error'],
                request.args['error_description'],
                response
            ))
            abort(401, 'There was a problem logging in')

        oauth_user = github_auth.get('user',
                                     token=(response['access_token'], ''))
        if oauth_user.status != 200:
            abort(401, 'Error logging in: could not get user details')
        oauth_user = oauth_user.data
        provider_id = oauth_user['id']

        # Check if user exists, first by provider id, then by email

        user = _get_user_by_provider_id(provider, provider_id)
        if not user:
            # User exists, but she had logged in with another provider
            user = _get_user_by_email(oauth_user['email'])

        if not user:
            # User does not exist, create it
            user = User(
                name=oauth_user['login'],
                display_name=oauth_user['name'],
                email=oauth_user['email']
            )

        if user.provider_ids is None:
            user.provider_ids = {}
        if user.conf is None:
            user.conf = {}

        # Update these values
        user.provider_ids.update({provider:  provider_id})
        user.github_oauth_token = response['access_token']

        database['session'].add(user)
        database['session'].commit()

        # TODO: check github scopes

        # Login user with Flask-Login
        login_user(user)

    return redirect(url_for('site.home'))
