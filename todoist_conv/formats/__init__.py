from todoist_conv.formats.base import Format
from todoist_conv.formats.json import JsonFormat
from todoist_conv.formats.opml import OpmlFormat
from todoist_conv.formats.csv import TodoistCsvFormat

_FORMATS = {
    "csv": TodoistCsvFormat,
    "opml": OpmlFormat,
    "json": JsonFormat,
}

FORMAT_NAMES = _FORMATS.keys()


def get_format(name: str) -> Format:
    return _FORMATS[name]()
