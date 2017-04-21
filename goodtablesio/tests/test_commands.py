import os

import pytest
from click.testing import CliRunner

from goodtablesio.commands import add_admin, remove_admin
from goodtablesio.tests import factories


def test_add_admin(flask_env):
    user = factories.User()

    assert user.admin is False

    runner = CliRunner()
    result = runner.invoke(add_admin, [user.name])

    assert result.exit_code == 0

    assert user.admin is True


def test_add_admin_with_id(flask_env):
    user = factories.User()

    assert user.admin is False

    runner = CliRunner()
    result = runner.invoke(add_admin, [user.id])

    assert result.exit_code == 0

    assert user.admin is True


def test_add_admin_missing_param(flask_env):

    runner = CliRunner()
    result = runner.invoke(add_admin)

    assert result.exit_code == 2
    assert 'Missing argument' in result.output


def test_add_admin_user_not_found(flask_env):

    runner = CliRunner()
    result = runner.invoke(add_admin, ['not-found'])

    assert result.exit_code == 1
    assert 'not found' in result.output


def test_remove_admin(flask_env):
    user = factories.User(admin=True)

    assert user.admin is True

    runner = CliRunner()
    result = runner.invoke(remove_admin, [user.name])

    assert result.exit_code == 0

    assert user.admin is False


def test_remove_admin_with_id(flask_env):
    user = factories.User(admin=True)

    assert user.admin is True

    runner = CliRunner()
    result = runner.invoke(remove_admin, [user.id])

    assert result.exit_code == 0

    assert user.admin is False


def test_remove_admin_missing_param(flask_env):

    runner = CliRunner()
    result = runner.invoke(remove_admin)

    assert result.exit_code == 2
    assert 'Missing argument' in result.output


def test_remove_admin_user_not_found(flask_env):

    runner = CliRunner()
    result = runner.invoke(remove_admin, ['not-found'])

    assert result.exit_code == 1
    assert 'not found' in result.output


@pytest.fixture
def flask_env():

    os.environ['FLASK_APP'] = 'goodtablesio/app.py'
    yield
    os.environ.pop('FLASK_APP', None)
