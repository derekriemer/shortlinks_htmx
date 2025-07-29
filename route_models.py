from __future__ import annotations
from pydantic import BaseModel, Field
from sqlmodel import Session

from models.entity import Shortcut
from helpers import get_shortcuts


class ShortcutsTable(BaseModel):
    filter: str = Field(default="")
    page: int = Field(ge=0)
    shortcuts: list[Shortcut] = Field()

    @classmethod
    # pylint: disable=W0622
    def get_shortcuts_table(cls, session: Session, page: int = 0, filter: str = "") -> ShortcutsTable:
        return ShortcutsTable(shortcuts=get_shortcuts(session, page=page, filter=filter), page=page, filter=filter)


class SingleShortcutPayload(BaseModel):
    name: str = Field()
    shortcut: Shortcut | None = Field()
