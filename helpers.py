from typing import Optional

from fastapi import HTTPException
from sqlmodel import select, Session

from models.entity import Link
from models.entity import Shortcut


def get_shortcuts(session: Session, filter: str | None = None, page: int = 0):
    if page < 0:
        raise ValueError("Pages must start at 0")
    query = select(Shortcut)
    if filter:
        query = query.where(
            Shortcut.name.like(F'%{filter}%'))
    # Search for 1 more row than needed to enable detection of a new page.
    # Some day, I will implement page number detection so  I can allow seeking to page
    # 1, 2, ... k, k+1, last.
    query = query.offset(page * 25).limit(26).order_by(Shortcut.name)
    results = session.exec(query)
    return results


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
    if shortcut.link.url != url:
        shortcut.link = Link(url=url)
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
