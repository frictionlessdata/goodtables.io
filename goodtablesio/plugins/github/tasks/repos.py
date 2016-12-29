import datetime
from goodtablesio.models.user import User
from goodtablesio.services import database
from goodtablesio.celery_app import celery_app
from goodtablesio.plugins.github.models.repo import GithubRepo
from goodtablesio.plugins.github.utils.repos import iter_repos_by_token
session = database['session']


# Module API

@celery_app.task(name='goodtablesio.github.collect_user_repositories')
def sync_user_repositories(user_id, token):
    """Sync user repositories.
    """
    # TODO: rewrite using sqlalchemy query
    session.execute(
        'DELETE FROM users_github_repos WHERE user_id = :user_id',
        {'user_id': user_id})
    user = session.query(User).get(user_id)
    for repo_data in iter_repos_by_token(token):
        repo = session.query(GithubRepo).get(repo_data['id'])
        if repo is None:
            repo = GithubRepo(**repo_data)
            session.add(repo)
        repo.active = repo_data['active']
        repo.updated = datetime.datetime.utcnow(),
        repo.users.append(user)
        # TODO: remove
        if repo_data['repo'] == 'example-goodtables.io':
            break
    session.commit()
