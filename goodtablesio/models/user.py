import logging
import datetime

from sqlalchemy import Column, Unicode, DateTime, Boolean, update as db_update
from sqlalchemy.dialects.postgresql import JSONB

from goodtablesio.services import database
from goodtablesio.models.base import Base, BaseModelMixin, make_uuid


log = logging.getLogger(__name__)


class User(Base, BaseModelMixin):

    __tablename__ = 'users'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    name = Column(Unicode, unique=True, nullable=False)
    email = Column(Unicode, unique=True, nullable=False)
    display_name = Column(Unicode)
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    admin = Column(Boolean, nullable=False, default=False)
    provider_ids = Column(JSONB)


def create(params):
    """
    Creates a user object in the database.

    Arguments:
        params (dict): A dictionary with the values for the new user.

    Returns:
        user (dict): The newly created user as a dict
    """

    user = User(**params)

    database['session'].add(user)
    database['session'].commit()

    log.debug('Created user "%s" on the database', user.id)
    return user.to_dict()


def update(params):
    """
    Updates a user object in the database.

    Arguments:
        params (dict): A dictionary with the fields to be updated. It must
            contain a valid `user_id` key.

    Returns:
        user (dict): The updated user as a dict

    Raises:
        ValueError: A `user_id` was not provided in the params dict.
    """

    user_id = params.get('id')
    if not user_id:
        raise ValueError('You must provide a id in the params dict')

    user = database['session'].query(User).get(user_id)
    if not user:
        raise ValueError('User not found: %s', user_id)

    user_table = User.__table__
    u = db_update(user_table).where(user_table.c.id == user_id).values(**params)

    database['session'].execute(u)
    database['session'].commit()

    log.debug('Updated user "%s" on the database', user_id)
    return user.to_dict()


def get(user_id):
    """
    Get a user object in the database and return it as a dict.

    Arguments:
        user_id (str): The user id.

    Returns:
        user (dict): A dictionary with the user details, or None if the user
            was not found.
    """

    user = database['session'].query(User).get(user_id)

    if not user:
        return None

    return user.to_dict()


def get_ids():
    """Get all user ids from the database.

    Returns:
        user_ids (str[]): A list of user ids, sorted by descending creation
        date.

    """

    user_ids = database['session'].query(User.id).order_by(User.created.desc()).all()
    return [j.id for j in user_ids]


def get_all():
    """Get all users in the database as dict.

    Warning: Use with caution, this should probably only be used in tests

    Returns:
        users (dict[]): A list of user dicts, sorted by descending creation
        date.

    """

    users = database['session'].query(User).order_by(User.created.desc()).all()
    return [j.to_dict() for j in users]
