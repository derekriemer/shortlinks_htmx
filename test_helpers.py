import pytest
from sqlmodel import Session, SQLModel, create_engine

from models.entity import Link
from models.entity import Shortcut
from helpers import get_shortcuts, find_shortcut, add_shortcut


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Fixture to add dummy data and commit


@pytest.fixture
def dummy_data(session):
    shortcuts = [
        Shortcut(name="foo", link=Link(url="https://foo.com")),
        Shortcut(name="bar", link=Link(url="https://bar.com")),
    ]
    for shortcut in shortcuts:
        session.add(shortcut)
    session.commit()
    # Optionally, refresh objects if needed
    for shortcut in shortcuts:
        session.refresh(shortcut)
    return shortcuts


def test_add_and_find_shortcut(session):
    shortcut = add_shortcut(session, "test", "https://example.com")
    session.commit()
    found = find_shortcut(session, "test")
    assert found is not None
    assert found.name == "test"
    assert found.link.url == "https://example.com"


def test_get_shortcuts_all(session):
    add_shortcut(session, "a", "https://a.com")
    add_shortcut(session, "b", "https://b.com")
    session.commit()
    results = list(get_shortcuts(session))
    assert len(results) == 2


def test_get_shortcuts_by_url(session):
    add_shortcut(session, "a", "https://a.com")
    add_shortcut(session, "b", "https://b.com")
    session.commit()
    results = list(get_shortcuts(session, url="https://a.com"))
    assert any(row[0].name == "a" for row in results)
    assert all(row[0].link.url == "https://a.com" for row in results)
