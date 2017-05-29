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
    github_orgs = []
    for repo_data in iter_repos_by_token(token):

        repo = database['session'].query(GithubRepo).filter(
            GithubRepo.name == repo_data['name']
        ).one_or_none()

        if repo and repo_data['conf']['private']:
            # TODO: check there's a valid subscription that this user can use
            # (eg for this GitHub organization)
            pass

        if repo is None:
            if (repo_data['conf']['private'] and
                    not _can_see_private_repos(user, repo_data)):
                continue

            repo = GithubRepo(**repo_data)
            database['session'].add(repo)

        repo.conf['private'] = repo_data['conf']['private']
        repo.active = repo_data['active']
        repo.updated = datetime.datetime.utcnow(),
        repo.users.append(user)

        org = repo.name.split('/')[0]
        if org not in github_orgs:
            github_orgs.append(org)

    # Update job
    job.status = 'success'
    job.finished = datetime.datetime.utcnow()

    # Update user's GitHub orgs
    user.conf['github_orgs'] = github_orgs

    # Commit to database
    database['session'].commit()


def _can_see_private_repos(user, repo_data):
    # TODO: check that there is any subscription that gives access to this
    # GitHub organization
    return (user.plan and user.plan.name != 'free') or user.admin
