from cement import Controller, ex
from ..models.models import Project
from sqlalchemy import select


class Projects(Controller):
    class Meta:
        label = "project"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list projects")
    def list(self):
        session = self.app.db_session
        projects = select(Project)
        for project in session.scalars(projects):
            print(project)

    @ex(help="add project", arguments=[(["project_name"], {"help": "project name"})])
    def add(self):
        project_name = self.app.pargs.project_name
        session = self.app.db_session
        project = Project(name=project_name)
        session.add(project)
        session.commit()

    @ex(help="delete project", arguments=[(["project_id"], {"help": "project id"})])
    def delete(self):
        project_id = self.app.pargs.project_id
        session = self.app.db_session
        project = session.query(Project).filter(Project.id == project_id)
        project.delete()
        session.commit()
