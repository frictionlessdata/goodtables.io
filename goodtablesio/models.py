# TODO: Right now these are just used for the tests factories, but eventually
# they will be SQLAlchemy models


class Job():

    job_id = None
    created = None
    finished = None
    report = None

    def __init__(self, *args, **kwargs):
        self.job_id = kwargs.get('job_id')
        self.created = kwargs.get('created')
        self.finished = kwargs.get('finished')
        self.report = kwargs.get('report')
