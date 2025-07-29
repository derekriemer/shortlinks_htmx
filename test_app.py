from sqlmodel import Session, select, text
from fastapi.testclient import TestClient

from models.entity import Link, Shortcut

test_shortcuts = [
    {


        "name": "derek",
        "url": "https://derekriemer.com",
    },
    {
        "name": "example",
        "url": "https://example.com",
    }
]


def fill_db(session: Session):
    for shortcut in test_shortcuts:
        session.add(
            Shortcut(name=shortcut['name'], link=Link(url=shortcut['url'])))
    session.commit()


def test_get_shortcuts_table(session: Session, client: TestClient, verify):
    fill_db(session)
    response = client.get("/htmx/shortcuts")
    verify(response.text)
    assert response.status_code == 200

# for each of the create, update operations, we have two endpoints.
# an endpoint to retreive dataa form to do operation.
# An endpoint to receive data from the form.
# This because it's not really feasible to have fastapi handle both post and get in one handler.


def test_add_page(client: TestClient, verify):
    response = client.get("/htmx/add/", headers={
        "hx-request": "true",
    })
    verify(response.text)
    assert response.status_code == 200


def test_add_form_commits_data(client: TestClient, session: Session, verify):
    response = client.post("/htmx/add_form/", data={
        "name": test_shortcuts[0]['name'],
        "url": test_shortcuts[0]['url'],
    })
    assert response.status_code == 200
    verify(response.text)
    shortcut = session.exec(select(Shortcut)).one()
    assert shortcut.name == test_shortcuts[0]['name']
    assert shortcut.link.url == test_shortcuts[0]['url']


def test_edit_page(session: Session, client: TestClient, verify):
    fill_db(session)
    response = client.get("/htmx/edit/", params={"name": "derek"})
    assert response.status_code == 200
    verify(response.text)


def test_edit_form(session: Session, client: TestClient, verify):
    fill_db(session)
    response = client.post("/htmx/edit_form/", params={
        "old_name": "derek",
    }, data={
        "name": "me",
        "url": "https://derekriemer.com",
    })
    assert response.status_code == 200
    verify(response.text)
    shortcut = session.exec(select(Shortcut).where(
        Shortcut.name == "me")).one()
    assert shortcut.name == "me"
    assert shortcut.link.url == "https://derekriemer.com"


def test_delete_page(client: TestClient, session: Session):
    fill_db(session)
    response = client.get("/htmx/delete/", params={"name": "example"})
    assert response.status_code == 200
