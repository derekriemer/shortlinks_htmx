import os

from dotenv import load_dotenv
from fastapi import FastAPI

import models
from api import router as api_router
from htmx_router import router as htmx_router
from route_models import ShortcutsTable
from fastx_globals import get_or_init_fastx

load_dotenv()

app = FastAPI()
jinja = get_or_init_fastx()

app.include_router(api_router, prefix="/api")
app.include_router(htmx_router, prefix="/htmx")


if os.environ.get("LOCAL_DEV"):
    # import late to avoid production imports.
    from fastapi.staticfiles import StaticFiles
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.on_event("startup")
def on_startup():
    models.create_db_and_tables()

# Special case this one, because I don't know of a way to mount a virtual / to an endpoint in the htmx_router.


@app.get("/")
@jinja.page("pages/index.html")
async def index(session: models.SessionDep) -> ShortcutsTable:
    return ShortcutsTable.get_shortcuts_table(session)
