import datetime
import os
from typing import Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
import jinja_partials
from fasthx import Jinja

load_dotenv()
templates = Jinja2Templates("templates")
jinja_partials.register_starlette_extensions(templates)
app = FastAPI()
jinja = Jinja(templates)


if os.environ.get("LOCAL_DEV"):
    # import late to avoid production imports.
    from fastapi.staticfiles import StaticFiles
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.get("/")
@jinja.page("pages/index.html")
def index() -> Dict[str, datetime.datetime]:
    
