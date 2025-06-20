# from typing import Annotated

# from fastapi import Depends, FastAPI
# from sqlmodel import SQLModel, Session, create_engine

# mysql_url = "mysql+mysqlconnector://root:@localhost/apiUno"
# engine = create_engine(mysql_url, echo=True)

# def create_all_tables(app: FastAPI):
#     SQLModel.metadata.create_all(engine)
#     yield

# def get_session():
#     with Session(engine) as session:
#         yield session
        
# SessionDep = Annotated[Session, Depends(get_session) ]


# PARA SQLITE -->>
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine

sqlite_url = "sqlite:///./db.sqlite3"
engine = create_engine(sqlite_url, echo=True)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]