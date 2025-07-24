from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .links import Link


class Shortcut(SQLModel, table=True):
    name: str = Field(primary_key=True)
    link_id: int = Field(foreign_key="link.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    access_count: int = Field(default=0)
    last_accessed: Optional[datetime] = None

    link: Optional[Link] = Relationship(back_populates="shortcuts")
