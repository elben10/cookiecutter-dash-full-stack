from pytest import fixture

from app.crud import CRUDUser
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.index import app as _app
from app.schemas import UserCreate


@fixture(scope="session")
def db_generator():
    Base.metadata.create_all(engine)


@fixture(scope="session")
def superuser(db_generator):
    db = SessionLocal()
    user_in = UserCreate(
        email="john@doe.com",
        password="changethis",
        password2="changethis",
        is_superuser=True,
    )
    if not CRUDUser.get_by_email(db, email="john@doe.com"):
        CRUDUser.create(db, user_in=user_in)
    db.close()


@fixture(scope="session")
def app(superuser):
    return _app
