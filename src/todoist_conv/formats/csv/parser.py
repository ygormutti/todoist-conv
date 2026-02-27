from todoist_conv.model import ProjectViewStyle
import re
from csv import DictReader
from datetime import datetime, timedelta
from pathlib import Path

from todoist_conv.formats.csv.common import FIELDNAMES, CsvRowFormat
from todoist_conv.model import Comment, Project, Section, Task, TaskDate, User


def parse(path: Path) -> Project:
    with open(path, newline="", encoding="utf-8-sig") as fp:
        reader = DictReader(fp, FIELDNAMES, "rest")
        next(reader)  # skip first row with field names
        return parse_project(path.stem, reader)


def parse_project(name, reader: DictReader):
    default_section = Section()
    state = ParserStateMachine(default_section)

    view_style = Project.__fields__["view_style"].default
    for row_dict in reader:
        if "rest" in row_dict:
            raise Exception(f"row {reader.line_num} has unknown format")

        non_empty_fields = {k: v for k, v in row_dict.items() if v != ""}
        row = CsvRowFormat(**non_empty_fields)

        match row.TYPE:
            case "meta":
                # FIXME meta field separator is unknown, docs only mention view_style
                view_style = ProjectViewStyle(row.CONTENT.split("=")[1])
            case "section":
                section = Section(
                    name=row.CONTENT,
                    is_collapsed=row.IS_COLLAPSED,
                )
                state.handle_section(section)
            case "task":
                task = Task(
                    name=row.CONTENT,
                    description=row.DESCRIPTION,
                    priority=row.PRIORITY,
                    author=parse_user(row.AUTHOR),
                    responsible=parse_user(row.RESPONSIBLE),
                    date=parse_task_date(row, "DATE"),
                    deadline=parse_task_date(row, "DEADLINE"),
                    duration=parse_duration(row),
                    timezone=row.TIMEZONE,
                )
                state.handle_task(task, int(row.INDENT))
            case "note":
                comment = Comment(
                    content=row.CONTENT,
                    author=parse_user(row.AUTHOR),
                    date=parse_iso_dt(row.DATE),
                )
                state.handle_note(comment)
            case "":
                continue  # ignore separator

    return Project(name=name, sections=state.sections, view_style=view_style)


USER_RE = re.compile(r"(?P<username>.*?) \((?P<id>.*?)\)")


def parse_user(user: str):
    if user is None:
        return

    m = USER_RE.match(user)
    return User(**m.groupdict())


def parse_task_date(row: CsvRowFormat, date_field: str):
    if getattr(row, date_field) is None:
        return

    return TaskDate(
        description=getattr(row, date_field),
        lang=getattr(row, f"{date_field}_LANG"),
    )


def parse_duration(row: CsvRowFormat):
    if row.DURATION is None:
        return

    assert row.DURATION_UNIT == "minute"

    return timedelta(minutes=row.DURATION)


def parse_iso_dt(dt_str: str):
    if dt_str is None:
        return

    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


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
        diff = self.indent - indent
        if diff > 0:  # indent decreased by diff
            for _ in range(diff):
                self.container_stack.pop()
        elif diff < 0:  # indent increased by 1
            assert diff == -1
            self.container_stack.append(self.task.subtasks)

        self.task = task
        self.indent = indent
        self.container_stack[-1].append(task)

    def handle_note(self, comment: Comment):
        self.task.comments.append(comment)
