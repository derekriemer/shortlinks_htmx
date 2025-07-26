from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str

    shortcut: list["Shortcut"] = Relationship(back_populates="link")


class Shortcut(SQLModel, table=True):
    name: str = Field(primary_key=True)
    link_id: int = Field(foreign_key="link.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    access_count: int = Field(default=0)
    last_accessed: Optional[datetime] = None

    link: Link | None = Relationship(back_populates="shortcut")
