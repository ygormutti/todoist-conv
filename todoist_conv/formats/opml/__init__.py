from todoist_conv.formats.base import Format
from todoist_conv.formats.opml.parser import parse
from todoist_conv.formats.opml.serializer import serialize
from todoist_conv.model import Project


class OpmlFormat(Format):
    def parse(self, path: str) -> Project:
        return parse(path)

    def serialize(self, project: Project) -> bytes:
        return serialize(project)
