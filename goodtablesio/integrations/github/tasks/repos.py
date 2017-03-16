import datetime
from goodtablesio.models.user import User
from goodtablesio.services import database
from goodtablesio.celery_app import celery_app
from goodtablesio.tasks.base import InternalJobTask
from goodtablesio.models.internal_job import InternalJob
from goodtablesio.integrations.github.models.repo import GithubRepo
from goodtablesio.integrations.github.utils.repos import iter_repos_by_token


@celery_app.task(name='goodtablesio.github.sync_user_repos',
        queue='internal', base=InternalJobTask)
def sync_user_repos(user_id, job_id):
    """Sync user repositories.
    """

    # Get user/job
    user = database['session'].query(User).get(user_id)
    job = database['session'].query(InternalJob).get(job_id)

    # Get token
    token = user.github_oauth_token
    if not token:
        raise ValueError('User don\'t have github auth token')

    # Update repos
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

    # Update job
    job.status = 'success'
    job.finished = datetime.datetime.utcnow()

    # Commit to database
    database['session'].commit()
