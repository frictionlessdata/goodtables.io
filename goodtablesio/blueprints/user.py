import logging

from flask import (
    Blueprint, request, session, redirect, url_for, abort, flash,
    render_template
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)

from goodtablesio import models
from goodtablesio.auth import github_auth


log = logging.getLogger(__name__)

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@login_required
def home():

    user = models.user.get(session['user_id'])

    return render_template('user.html', user=user)


@user.route('/login/<any(github):provider>')
def login(provider):
    if current_user.is_authenticated:
        flash('You are already logged in. Please log out if you want to ' +
              'log in with a different account', 'warning')
        return redirect(url_for('site.home'))

    # TODO: redirect to "next"

    callback_url = url_for('user.authorized', provider=provider,
                           _external=True)
    if provider == 'github':
        return github_auth.authorize(callback=callback_url)


@user.route('/logout')
def logout():

    # Clear user session
    session.clear()

    # Logout user with Flask-Login
    logout_user()

    return redirect(url_for('site.home'))


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

        session['auth_github_token'] = (response['access_token'], '')

        oauth_user = github_auth.get('user')
        if oauth_user.status != 200:
            abort(401, 'Error logging in: could not get user details')
        oauth_user = oauth_user.data
        provider_id = oauth_user['id']

        # Check if user exists, first by provider id, then by email

        user = models.user.get_by_provider_id(provider, provider_id)
        if not user:
            user = models.user.get_by_email(oauth_user['email'])
            if user:
                # User exists, but she had logged in with another provider
                user['provider_ids'].update({provider: provider_id})
                user = models.user.update({
                    'id': user['id'],
                    'provider_ids': user['provider_ids']})

        # User does not exist, create it
        if not user:
            user = models.user.create({
                'name': oauth_user['login'],
                'display_name': oauth_user['name'],
                'email': oauth_user['email'],
                'provider_ids': {'github': oauth_user['id']},
            })

        # TODO: check github scopes

        # Login user with Flask-Login
        # (we need the actual model object)
        login_user(models.user.get(user['id'], as_dict=False))

    return redirect(url_for('site.home'))
