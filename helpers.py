from typing import Optional

from fastapi import HTTPException
from sqlmodel import select, Session

from models.entity import Link
from models.entity import Shortcut


def get_shortcuts(session: Session, url: Optional[str] = None):
    query = select(Shortcut)
    if url:
        query = query.where(Shortcut.link.url == url)
    return session.exec(query)


def find_shortcut(session: Session, name: str):
    return session.exec(select(Shortcut).where(Shortcut.name == name)).first()


def add_shortcut(session: Session, name: str, url: str):
    with session.begin():
        link = Link(url=url)
        shortcut = Shortcut(name=name, link=link)
        session.add(shortcut)
    session.refresh(shortcut)
    return shortcut


def edit_shortcut(session: Session, old_name: str, name: str, url: str):
    shortcut = find_shortcut(session, old_name)
    if not shortcut:
        raise HTTPException(status_code=404, detail="Shortcut not found")
    shortcut.name = name
    shortcut.link.url = url
    session.add(shortcut)
    session.commit()
    session.refresh(shortcut)
    return shortcut


def delete_shortcut(session: Session, name: str):
    shortcut = find_shortcut(session, name)
    if not shortcut:
        raise HTTPException(status_code=404, detail="Shortcut not found")
    session.delete(shortcut)
    session.commit()
