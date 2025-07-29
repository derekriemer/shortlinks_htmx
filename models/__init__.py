import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel

sqlite_file_name = "golinks.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    try:
        with Session(engine) as session:
            yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]
