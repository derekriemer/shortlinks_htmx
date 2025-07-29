import pytest
from sqlmodel import Session

from models.entity import Link
from models.entity import Shortcut
from helpers import get_shortcuts, find_shortcut


def add_and_commit(session, *objects):
    """Local helper to add objects and commit"""
    for obj in objects:
        session.add(obj)
    session.commit()
    for obj in objects:
        session.refresh(obj)
    return objects


# Fixture to add dummy data and commit

@pytest.fixture
def dummy_data(session):
    shortcuts = [
        Shortcut(name="foo", link=Link(url="https://foo.com")),
        Shortcut(name="bar", link=Link(url="https://bar.com")),
    ]
    add_and_commit(session, *shortcuts)
    return shortcuts


def test_add_and_find_shortcut(session,
                               # pylint:disable=all
                               dummy_data):
    found = find_shortcut(session, "foo")
    assert found is not None
    assert found.name == "foo"
    assert found.link.url == "https://foo.com"


def test_get_shortcuts_all(session: Session,
                           # pylint:disable=all
                           dummy_data):
    results = get_shortcuts(session).all()
    assert len(results) == 2
