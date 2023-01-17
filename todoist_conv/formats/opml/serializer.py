import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

from todoist_conv.model import Project, Task


def serialize(project: Project) -> bytes:
    opml = build_opml(project)
    doc = ET.ElementTree(opml)
    buffer = BytesIO()
    doc.write(buffer, encoding="utf-8", xml_declaration=True)
    return buffer.getvalue()


def build_opml(project: Project) -> ET.Element:
    opml = ET.Element("opml", version="2.0")
    build_head(opml, project.name)
    build_body(opml, project)
    ET.indent(opml)
    return opml


def build_head(opml, title):
    head = ET.SubElement(opml, "head")

    title_elem = ET.SubElement(head, "title")
    title_elem.text = title

    dateCreated = ET.SubElement(head, "dateCreated")
    dateCreated.text = datetime.now().isoformat()


def build_body(opml, project: Project):
    body = ET.SubElement(opml, "body")

    project_outline = build_outline(body, project.name)

    for section in project.sections:
        section_outline = build_outline(project_outline, section.name or "")
        for task in section.tasks:
            build_task_outlines(section_outline, task)


def build_outline(parent, text, description=None):
    outline = ET.SubElement(parent, "outline", text=text)
    if description:
        outline.attrib["description"] = description
    return outline


def build_task_outlines(parent: ET.Element, task: Task):
    task_elem = build_outline(
        parent, task.name, task.copy(exclude={"subtasks"}, deep=True).json()
    )
    for subtask in task.subtasks:
        build_task_outlines(task_elem, subtask)
