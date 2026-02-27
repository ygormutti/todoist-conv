from pathlib import Path

from todoist_conv.formats.base import Format
from todoist_conv.formats.csv.parser import parse
from todoist_conv.formats.csv.serializer import serialize
from todoist_conv.model import Project


class TodoistCsvFormat(Format):
    def parse(self, path: Path) -> Project:
        return parse(path)

    def serialize(self, project: Project) -> str:
        return serialize(project)
