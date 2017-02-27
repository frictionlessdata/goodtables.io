from goodtablesio.models.source import Source


class GithubRepo(Source):

    __mapper_args__ = {
        'polymorphic_identity': 'github'
    }

    def to_api(self):
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
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
