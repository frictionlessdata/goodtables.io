import sys

import click

from goodtablesio.app import app
from goodtablesio.services import database
from goodtablesio.models.user import User


@app.cli.command()
@click.argument('username')
def add_admin(username):
    """Give an existing user admin permissions."""
    user = _get_user(username)

    user.admin = True
    database['session'].add(user)
    database['session'].commit()

    click.echo('Added user `{}` as admin'.format(username))


@app.cli.command()
@click.argument('username')
def remove_admin(username):
    """Remove admin permissions an existing user."""

    user = _get_user(username)

    user.admin = False
    database['session'].add(user)
    database['session'].commit()

    click.echo('Removed admin permissions from user `{}`'.format(username))


def _get_user(user_name):

    user = database['session'].query(User).filter(
        (User.id == user_name) | (User.name == user_name)).one_or_none()

    if not user:
        click.echo('User `{}` not found'.format(user_name))
        sys.exit(1)

    return user
