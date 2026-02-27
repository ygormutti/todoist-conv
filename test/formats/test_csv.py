from pathlib import Path

from todoist_conv.formats import TodoistCsvFormat


import pytest


@pytest.fixture
def weekly_review_project():
    return TodoistCsvFormat().parse(Path("test/data/Weekly Review.csv"))


def test_csv_parser(weekly_review_project, snapshot):
    assert weekly_review_project == snapshot


def test_csv_serializer(weekly_review_project, snapshot):
    actual = TodoistCsvFormat().serialize(weekly_review_project)
    assert actual == snapshot


def test_csv_end_to_end(weekly_review_project):
    actual = TodoistCsvFormat().serialize(weekly_review_project)
    assert actual == Path("test/data/Weekly Review.csv").read_bytes()
