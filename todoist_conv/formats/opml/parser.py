import xml.etree.ElementTree as ET

from todoist_conv.model import Project, Section, Task


def parse(path: str) -> Project:
    tree = ET.parse(path)
    project_elem = tree.getroot().find("body/outline")

    name = get_name(project_elem)
    sections = parse_sections(get_children(project_elem))

    return Project(name=name, sections=sections)


def get_name(outline_elem):
    return outline_elem.get("text")


def get_children(outline_elem):
    return outline_elem.findall("outline")


def parse_sections(section_elems: list[ET.Element]) -> list[Section]:
    sections = []
    for section_elem in section_elems:
        name = get_name(section_elem)
        tasks = parse_tasks(get_children(section_elem))
        sections.append(Section(name=name, tasks=tasks))

    return sections


def parse_tasks(task_elems: list[ET.Element]) -> list[Task]:
    tasks = []
    for task_elem in task_elems:
        subtasks = parse_tasks(get_children(task_elem))
        task_json = task_elem.get("description")
        task = Task.parse_raw(task_json) if task_json else Task(name="", priority=4)
                
        task.name = get_name(task_elem)
        task.subtasks.extend(subtasks)
        tasks.append(task)

    return tasks
