from dash import Dash
from flask_login import LoginManager

from app.config import config
from app.crud import CRUDUser
from app.db.session import SessionLocal

CSS = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css",
    "https://cdn.datatables.net/1.10.23/css/dataTables.bootstrap4.min.css",
]
JS = [
    "https://code.jquery.com/jquery-3.5.1.slim.min.js",
    "https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js",
]

app = Dash(
    __name__,
    external_scripts=JS,
    external_stylesheets=CSS,
    suppress_callback_exceptions=True,
)
server = app.server

server.config.update(
    SECRET_KEY=config.SECRET_KEY,
)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    try:
        return CRUDUser.get(db, id=user_id)
    finally:
        db.close()