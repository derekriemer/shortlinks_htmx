from typing import Annotated

from fastapi import APIRouter, Query, Form
from fasthx import Jinja
from fastx_globals import get_or_init_fastx

from htmx_component_selector import HTMXComponentSelector
from route_models import ShortcutsTable
from models.entity import Shortcut
import models
from helpers import add_shortcut, delete_shortcut, edit_shortcut, find_shortcut, get_shortcuts

router = APIRouter()
jinja = get_or_init_fastx()


@router.get("/shortcuts")
@jinja.page(HTMXComponentSelector("pages/index.html", "partials/table.html"))
async def get_shortcuts_table(session: models.SessionDep,
                              page: Annotated[int, Query(ge=0)] = 0,
                              shortcut_filter: Annotated[str, Query(regex=r"[a-zA-Z0-9_]*")] = "") -> ShortcutsTable:
    return ShortcutsTable(shortcuts=get_shortcuts(session, page=page, filter=shortcut_filter).all(), filter=shortcut_filter, page=page)


@router.get("/add/")
@jinja.page("pages/add.html")
async def add():
    ...


@router.post("/add_form/")
@jinja.page("pages/index.html")
async def form_add(
    session: models.SessionDep,
        name: Annotated[str, Form()],
        url: Annotated[str, Form()]) -> ShortcutsTable:
    add_shortcut(session, name, url)
    return ShortcutsTable.get_shortcuts_table(session)


@router.get("/edit/")
@jinja.page("pages/edit.html")
async def edit(session: models.SessionDep, name: Annotated[str, Query()]) -> Shortcut:
    return find_shortcut(session, name)


# fixme: pydantic.AfterValidator in the annotation to catch urls.
# I can't be arsed right now to write an exception converter.
@router.post("/edit_form/")
@jinja.page("pages/index.html")
async def form_edit(
        session: models.SessionDep,
        old_name: Annotated[str, Query()],
        name: Annotated[str, Form()],
        url: Annotated[str, Form()]) -> ShortcutsTable:
    edit_shortcut(session, old_name, name, url)
    return ShortcutsTable.get_shortcuts_table(session)


# no fastx decoration, this endpoint uses status alone to communicate.
@router.get("/delete/")
async def delete(session: models.SessionDep, name: Annotated[str, Query()]):
    delete_shortcut(session, name)
