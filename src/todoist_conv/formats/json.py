from pathlib import Path
from todoist_conv.formats.base import Format
from todoist_conv.model import Project


class JsonFormat(Format):
    def parse(self, path: Path) -> Project:
        with open(path) as json_fp:
            return Project.parse_raw(json_fp.read())

    def serialize(self, project: Project) -> bytes:
        return project.json(indent=2).encode()
