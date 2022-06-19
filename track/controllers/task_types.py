from cement import Controller, ex
from ..models.models import TaskType
from sqlalchemy import select

class TaskTypes(Controller):
    class Meta:
        label = "type"
        stacked_type = "nested"
        stacked_on = "task"

    @ex(help="list task types")
    def list(self):
        session = self.app.db_session
        task_types = select(TaskType)
        for task_type in session.scalars(task_types):
            print(task_type)

    @ex(help="add task type", arguments=[(["task_type_name"], {"help": "task type name"})])
    def add(self):
        task_type_name = self.app.pargs.task_type_name
        session = self.app.db_session
        task_type = TaskType(name=task_type_name)
        session.add(task_type)
        session.commit()
