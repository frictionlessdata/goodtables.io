# TODO: Right now these are just used for the tests factories, but eventually
# they will be SQLAlchemy models


class Job():

    job_id = None
    status = 'created'
    plugin_name = 'api'
    plugin_conf = None
    created = None
    finished = None
    report = None
    error = None

    def __init__(self, *args, **kwargs):
        self.job_id = kwargs.get('job_id')
        self.status = kwargs.get('status', 'created')
        self.plugin_name = kwargs.get('plugin_name', 'api')
        self.plugin_conf = kwargs.get('plugin_conf')
        self.created = kwargs.get('created')
        self.finished = kwargs.get('finished')
        self.report = kwargs.get('report')
        self.error = kwargs.get('error')
