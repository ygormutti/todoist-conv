from abc import ABC, abstractmethod
from pathlib import Path
from todoist_conv.model import Project


class Format(ABC):
    name = None

    @abstractmethod
    def parse(self, path: Path) -> Project:
        pass

    @abstractmethod
    def serialize(self, project: Project) -> bytes:
        pass
