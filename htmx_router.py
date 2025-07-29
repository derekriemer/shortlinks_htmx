from typing import Annotated

from fastapi import APIRouter, Form, Query, status
from fastapi.responses import RedirectResponse
from fasthx import Jinja

import models
from fastx_globals import get_or_init_fastx
from helpers import (add_shortcut, delete_shortcut, edit_shortcut,
                     find_shortcut, get_shortcuts)
from htmx_component_selector import HTMXComponentSelector
from models.entity import Shortcut
from route_models import ShortcutsTable, SingleShortcutPayload

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
async def form_add(
        session: models.SessionDep,
        name: Annotated[str, Form()],
        url: Annotated[str, Form()]) -> RedirectResponse:
    try:
        add_shortcut(session, name, url)
    except ValueError:

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/edit/")
@jinja.page("pages/edit.html")
async def edit(session: models.SessionDep, name: Annotated[str, Query()]) -> SingleShortcutPayload:
    return SingleShortcutPayload(shortcut=find_shortcut(session, name), name=name)


# fixme: pydantic.AfterValidator in the annotation to catch urls.
# I can't be arsed right now to write an exception converter.
@router.post("/edit_form/")
async def form_edit(
        session: models.SessionDep,
        old_name: Annotated[str, Query()],
        name: Annotated[str, Form()],
        url: Annotated[str, Form()]) -> RedirectResponse:
    edit_shortcut(session, old_name, name, url)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


# no fastx decoration, this endpoint uses status alone to communicate.
@router.get("/delete/")
async def delete(session: models.SessionDep, name: Annotated[str, Query()]):
    delete_shortcut(session, name)
