from typing import Annotated, List, Optional

from fastapi import APIRouter, Path, Query
from pydantic import AfterValidator
from sqlmodel import select

import models
from helpers import add_shortcut, delete_shortcut, edit_shortcut, find_shortcut, get_shortcuts
from validation_helpers import validate_url

from models.entity import Shortcut

router = APIRouter()


@router.get("/shortcuts")
def shortcuts(session: models.SessionDep) -> List[Shortcut]:
    return get_shortcuts(session).all()


@router.get("/shortcut/{name}")
def get_shortcut(session: models.SessionDep, name: Annotated[Optional[str], Path()]) -> List[Shortcut]:
    return find_shortcut(session, name)


@router.post("/add")
def add(
        session: models.SessionDep,
        name: str,
        url: Annotated[str, Query()]) -> Shortcut:
    shortcut = add_shortcut(session, name, url)
    return shortcut


@router.put("/edit/")
def edit(session: models.SessionDep,
         old_name: Annotated[str, Query()],
         name: Annotated[str, Query()],
         url: Annotated[str, Query(), AfterValidator(validate_url)]) -> Shortcut:
    return edit_shortcut(session, old_name, name, url)


@router.delete("/delete/")
def delete(session: models.SessionDep, name: Annotated[str, Query()]) -> None:
    delete_shortcut(session, name)
