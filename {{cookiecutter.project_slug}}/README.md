# {{cookiecutter.project_name}}

Do the following to initialize the project

- Set the following environment variables
  - FLASK_APP=app.index:server
  - FLASK_ENV=development
  - SQLALCHEMY_DATABASE_URI=sqlite:///foo.db
- Instal poetry ([Instructions](https://python-poetry.org/docs/#installation))
- Run `poetry install`
- RUN `poetry run flask run`
- RUN the following script

  ```python
  from app.crud import CRUDUser
  from app.db.session import SessionLocal
  from app.schemas import UserCreate
  from app.db.base import Base
  from app.db.session import engine

  Base.metadata.create_all(engine)

  db = SessionLocal()
  user_in = UserCreate(email="john@doe.com", password="changethis", password2="changethis", is_superuser=True)
  user = CRUDUser.create(db, user_in=user_in)
  ```

- Go to http://localhost:5000 and login
