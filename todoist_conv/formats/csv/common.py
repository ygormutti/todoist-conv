from typing import Optional

from pydantic import BaseModel, conint

ENCODING = "utf-8-sig"


class CsvRowFormat(BaseModel):
    """Defines the expected column order and format in Todoist CSVs"""

    TYPE: Optional[str]
    CONTENT: Optional[str]
    DESCRIPTION: Optional[str]
    IS_COLLAPSED: Optional[str]
    PRIORITY: Optional[conint(strict=False, ge=1, le=4)]
    INDENT: Optional[conint(strict=False, ge=1)]
    AUTHOR: Optional[str]
    RESPONSIBLE: Optional[str]
    DATE: Optional[str]
    DATE_LANG: Optional[str]
    TIMEZONE: Optional[str]
    DURATION: Optional[int]
    DURATION_UNIT: Optional[str]
    DEADLINE: Optional[str]
    DEADLINE_LANG: Optional[str]


FIELDNAMES = CsvRowFormat.__fields__.keys()
