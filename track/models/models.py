from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship("Task", back_populates="projects")

    def __repr__(self) -> str:
        return f"Project id: {self.id!r}; Project name: {self.name!r}"


class TaskType(Base):
    __tablename__ = "tasktypes"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship("Task", back_populates="tasktypes")

    def __repr__(self) -> str:
        return f"Task type id: {self.id!r}; Task type name: {self.name!r}"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    project = Column(Integer, ForeignKey("projects.id"))
    type = Column(Integer, ForeignKey("tasktypes.id"))

    projects = relationship("Project", back_populates="tasks")
    tasktypes = relationship("TaskType", back_populates="tasks")
    works = relationship("Work", back_populates="tasks")


class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    task = Column(Integer, ForeignKey("tasks.id"))
    start = Column(DateTime)
    end = Column(DateTime)
    duration = Column(Integer)

    tasks = relationship("Task", back_populates="works")
