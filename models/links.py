from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .shortcut import Shortcut


class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str

    shortcuts: list["Shortcut"] = Relationship(back_populates="link")
