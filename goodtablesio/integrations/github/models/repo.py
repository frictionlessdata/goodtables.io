from goodtablesio.models.project import Project


class GithubRepo(Project):

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
