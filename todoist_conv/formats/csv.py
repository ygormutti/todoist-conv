import re

from csv import DictReader
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, conint
from todoist_conv.formats.base import Format
from todoist_conv.model import Comment, Project, Section, Task, TaskDate, User


class CsvRowFormat(BaseModel):
    TYPE: str
    CONTENT: str
    DESCRIPTION: str
    PRIORITY: conint(ge=1, le=4)
    INDENT: conint(ge=1)
    AUTHOR: str
    RESPONSIBLE: str
    DATE: str
    DATE_LANG: str
    TIMEZONE: str


AUTHOR_RE = re.compile(r"(?P<username>.*?) \((?P<id>.*?)\)")


def parse_user(author: str):
    m = AUTHOR_RE.match(author)
    return User(**m.groupdict())


class TodoistCsvFormat(Format):
    def parse(self, path: Path) -> Project:
        with open(path, newline="") as fp:
            reader = DictReader(fp, CsvRowFormat.__fields__.keys())
            sections = self.parse_sections(reader)

        return Project(name=path.stem, sections=sections)

    def parse_sections(self, reader):
        default_section = Section()
        state = ParserStateMachine(default_section)

        for row_dict in reader:
            row = CsvRowFormat(**row_dict)

            match row.TYPE:
                case "section":
                    section = Section(row.CONTENT)
                    state.handle_section(section)
                case "task":
                    task = Task(
                        name=row.CONTENT,
                        description=row.DESCRIPTION,
                        priority=row.PRIORITY,
                        author=parse_user(row.AUTHOR),
                        responsible=parse_user(row.RESPONSIBLE),
                        date=TaskDate(row.DATE, row.DATE_LANG, row.TIMEZONE),
                    )
                    state.handle_task(task, row.INDENT)
                case "note":
                    comment = Comment(
                        content=row.CONTENT,
                        author=parse_user(row.AUTHOR),
                        date=datetime.fromisoformat(row.DATE),
                    )
                    state.handle_note(comment)
                case "":
                    continue  # ignore separator

        return state.sections

    def serialize(self, project: Project) -> str:
        raise NotImplementedError()


class ParserStateMachine:
    def __init__(self, default_section: Section) -> None:
        self.sections = []
        self.handle_section(default_section)

    def handle_section(self, section: Section):
        self.sections.append(section)
        self.container_stack = [section.tasks]
        self.indent = 1
        self.task = None

    def handle_task(self, task: Task, indent: int):
        # same indent => pop container from previous task only
        # lower indent => pop containers from previous and dedented tasks
        # higher indent => pop nothing (self.indent - indent + 1 <= 0)
        for _ in range(self.indent - indent + 1):
            self.container_stack.pop()

        self.task = task
        self.indent = indent
        self.container_stack[-1].append(task)

        # next task could be a subtask, so we always push the container
        self.container_stack.append(task.subtasks)

    def handle_note(self, comment: Comment):
        self.task.comments.append(comment)
