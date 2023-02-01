from csv import DictWriter
from io import StringIO
from typing import List

from todoist_conv.formats.csv.common import ENCODING, FIELDNAMES, CsvRowFormat
from todoist_conv.model import Project, Section, Task, User


def serialize(project: Project) -> bytes:
    buffer = StringIO(newline="")
    dw = DictWriter(buffer, FIELDNAMES)
    dw.writeheader()
    write_sections(dw, project.sections)
    return buffer.getvalue().encode(ENCODING)


def write_sections(dw: DictWriter, sections: List[Section]):
    default_section = next(s for s in sections if s.isdefault)
    write_tasks(dw, default_section.tasks)

    for section in sections:
        if section.isdefault:
            continue

        dw.writerow(CsvRowFormat(TYPE="section").dict())
        write_tasks(dw, section.tasks)


def write_tasks(dw: DictWriter, tasks: List[Task], indent: int = 1):
    for task in tasks:
        write_task(dw, task, indent)


def write_task(dw: DictWriter, task: Task, indent: int):
    row = CsvRowFormat(
        TYPE="task",
        CONTENT=task.name,
        DESCRIPTION=task.description,
        PRIORITY=task.priority,
        INDENT=indent,
        AUTHOR=serialize_user(task.author),
        RESPONSIBLE=serialize_user(task.responsible),
        DATE=task.date and task.date.description,
        DATE_LANG=task.date and task.date.lang,
        TIMEZONE=task.date and task.date.timezone,
    )
    dw.writerow(row.dict())

    for comment in task.comments:
        comment_row = CsvRowFormat(
            TYPE="note",
            CONTENT=comment.content,
            AUTHOR=serialize_user(comment.author),
            DATE=serialize_iso_dt(comment.date),
        )
        dw.writerow(comment_row.dict())

    dw.writerow({})  # separator
    write_tasks(dw, task.subtasks, indent + 1)


def serialize_user(user: User):
    if user is None:
        return None
    return f"{user.username} ({user.id})"


def serialize_iso_dt(date):
    return date.isoformat().replace("+00:00", "Z")
