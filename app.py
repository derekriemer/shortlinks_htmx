import os
from typing import Annotated, List, Optional

import jinja2
import jinja_partials
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Path, Query
from fastapi.templating import Jinja2Templates
from fasthx import Jinja
from pydantic import AfterValidator
from sqlmodel import select
import validators

import models
from models.entity import Shortcut
from helpers import add_shortcut, delete_shortcut, edit_shortcut, find_shortcut, get_shortcuts


load_dotenv()
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    extensions=[
        "jinja2.ext.debug",
    ]
)
templates = Jinja2Templates(env=env)

jinja_partials.register_starlette_extensions(templates)
app = FastAPI()
jinja = Jinja(templates)


if os.environ.get("LOCAL_DEV"):
    # import late to avoid production imports.
    from fastapi.staticfiles import StaticFiles
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.on_event("startup")
def on_startup():
    models.create_db_and_tables()


@app.get("/")
@jinja.page("pages/index.html")
def index(session: models.SessionDep) -> List[Shortcut]:
    return session.exec(select(Shortcut)).all()


@app.get("/add/")
@jinja.page("pages/add.html")
def add():
    ...


@app.post("/add_form/")
@jinja.hx("pages/index.html")
def form_add(
        session: models.SessionDep,
        name: Annotated[str, Form()],
        url: Annotated[str, Form()]) -> List[Shortcut]:
    add_shortcut(session, name, url)
    return get_shortcuts(session).all()


@app.get("/edit/")
@jinja.page("pages/edit.html")
def edit(session: models.SessionDep, name: Annotated[str, Query()]) -> Shortcut:
    return find_shortcut(session, name)


# fixme: pydantic.AfterValidator in the annotation to catch urls.
# I can't be arsed right now to write an exception converter.
@app.post("/edit_form/")
@jinja.hx("pages/index.html")
def form_edit(
        session: models.SessionDep,
        old_name: Annotated[str, Query()],
        name: Annotated[str, Form()],
        url: Annotated[str, Form()]) -> List[Shortcut]:
    edit_shortcut(session, old_name, name, url)
    return get_shortcuts(session).all()


@app.get("/delete/")
def delete(session: models.SessionDep, name: Annotated[str, Query()]):
    delete_shortcut(session, name)
