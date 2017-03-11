import datetime
from celery import Task as CeleryTask
from goodtablesio.models.task import Task as TaskModel
from goodtablesio.services import database


# Module API

class Task(CeleryTask):
    """Base class for all internal tasks.
    """

    # Public

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """This handler is responsible to catch all task exceptions.
        """

        # Get error message
        message = str(exc)

        # Update database
        task = database['session'].query(TaskModel).get(task_id)
        if task:
            task.status = 'error'
            task.finished = datetime.datetime.utcnow()
            task.error = {'message': message}
            database['session'].commit()
