import datetime
from goodtablesio.models.user import User
from goodtablesio.services import database
from goodtablesio.celery_app import celery_app
from goodtablesio.integrations.github.models.repo import GithubRepo
from goodtablesio.integrations.github.utils.repos import iter_repos_by_token


@celery_app.task(name='goodtablesio.github.sync_user_repos')
def sync_user_repos(user_id, token):
    """Sync user repositories.
    """
    user = database['session'].query(User).get(user_id)

    for repo_data in iter_repos_by_token(token):
        repo = database['session'].query(GithubRepo).filter(
            GithubRepo.conf['github_id'].astext == repo_data['conf']['github_id']
        ).one_or_none()
        if repo is None:
            repo = GithubRepo(**repo_data)
            database['session'].add(repo)
        repo.active = repo_data['active']
        repo.updated = datetime.datetime.utcnow(),
        repo.users.append(user)
    database['session'].commit()
