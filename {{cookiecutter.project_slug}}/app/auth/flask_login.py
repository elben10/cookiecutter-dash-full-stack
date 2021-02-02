from flask import redirect, render_template, request
from flask_login import current_user, login_user

from app.auth.auth import Auth
from app.crud import CRUDUser
from app.db.session import SessionLocal


class FlaskLogin(Auth):
    def __init__(self, app):
        super().__init__(app)

        @app.server.route("/login", methods=["GET", "POST"])
        def login_route():
            error = False
            if self.is_authorized():
                return redirect("/")
            else:
                if request.method == "POST":
                    db = SessionLocal()
                    email = request.form.get("email")
                    password = request.form.get("password")
                    rememberMe = request.form.get("rememberMe") is not None
                    try:
                        user = CRUDUser.authenticate(db, email=email, password=password)
                        if user:
                            login_user(user, remember=rememberMe)
                            return redirect("/")
                    finally:
                        db.close()
                    error = True
                return render_template("login.html", error=error)

    def is_authorized(self):
        # Is the user authenticated?
        return current_user.is_authenticated

    def login_request(self):
        # Response if the user is not autenticated
        return redirect("/login")

    def auth_wrapper(self, f):
        # Wraps all other views than the dash view that is
        # added before super method is called in the init method
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return f(*args, **kwargs)
            else:
                return self.login_request()

        return wrap

    def index_auth_wrapper(self, original_index):
        # Wraps the dash view
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()

        return wrap
