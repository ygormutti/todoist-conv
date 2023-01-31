from datetime import datetime

from pydantic import BaseModel, conint


class User(BaseModel):
    username: str
    id: int


class TaskDate(BaseModel):
    description: str
    lang: str
    timezone: str


class Comment(BaseModel):
    content: str
    author: User
    date: datetime


class Task(BaseModel):
    name: str
    priority: conint(ge=1, le=4)

    description: str = None
    author: User = None
    responsible: User = None
    date: TaskDate = None
    comments: list[Comment] = []
    subtasks: list["Task"] = []


class Section(BaseModel):
    name: str = None
    tasks: list[Task] = []

    @property
    def isdefault(self):
        return not self.name


class Project(BaseModel):
    name: str

    sections: list[Section] = []
