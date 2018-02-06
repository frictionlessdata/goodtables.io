import logging
from goodtablesio.services import database
from goodtablesio.models.base import make_uuid
from goodtablesio.models.job import Job
from goodtablesio.models.source import Source
from goodtablesio.integrations.github.utils.status import set_commit_status
from goodtablesio.integrations.github.utils.validation import run_validation
from goodtablesio.integrations.github.utils.repos import get_default_repo_details
log = logging.getLogger(__name__)


# Module API

class GithubRepo(Source):

    __mapper_args__ = {
        'polymorphic_identity': 'github'
    }

    @property
    def url(self):
        parts = self.name.split('/')
        template = 'https://github.com/{owner}/{repo}'
        return template.format(owner=parts[0], repo=parts[1])

    @property
    def owner(self):
        parts = self.name.split('/')
        return parts[0]

    @property
    def repo(self):
        parts = self.name.split('/')
        return parts[1]

    @property
    def tokens(self):
        return [user.github_oauth_token for user in self.users
            if user.github_oauth_token]

    def create_and_start_job(self, conf=None):

        # Get tokens
        if not self.tokens:
            log.error('No GitHub tokens available to perform the job')
            return None

        # Get default repo details
        if not conf:
            conf = get_default_repo_details(self.owner, self.repo, token=self.tokens[0])
            if not conf:
                log.error('No default repo details are available')
                return None

        # Save job to database
        job_id = make_uuid()
        params = {
            'id': job_id,
            'integration_name': 'github',
            'source_id': self.id,
            'conf': conf
        }
        job = Job(**params)
        job.source = self
        database['session'].add(job)
        database['session'].commit()

        # Set GitHub status
        set_commit_status(
            'pending',
            owner=conf['owner'],
            repo=conf['repo'],
            sha=conf['sha'],
            job_number=job.number,
            is_pr=conf['is_pr'],
            tokens=self.tokens)

        # Run validation
        run_validation(conf['owner'], conf['repo'], conf['sha'],
            job_id=job_id, tokens=self.tokens)

        return job_id
