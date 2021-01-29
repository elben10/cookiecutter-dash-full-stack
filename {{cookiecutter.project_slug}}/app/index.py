import re

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from flask_login import current_user, logout_user

from app import views
from app.app import app, server
from app.crud import CRUDUser
from app.db.session import SessionLocal

app.layout = html.Div(
    [
        dcc.Location(id="urlNoRefresh"),
        dcc.Location(id="urlRefresh", refresh=True),
        html.Div(id="content"),
    ]
)
sidebar_context = [
    {"title": "Dashboard", "href": "/", "icon": "fas fa-fw fa-tachometer-alt"},
]


@app.callback(Output("content", "children"), [Input("urlNoRefresh", "pathname")])
def route(pathname):
    if current_user.is_authenticated:
        if pathname == "/":
            return views.home.layout(sidebar_context)
        elif pathname == "/users/profile":
            return views.users_profile.layout(sidebar_context)
        if current_user.is_superuser:
            if pathname == "/users":
                return views.users.layout(sidebar_context)
            elif pathname == "/users/create":
                return views.users_create.layout(sidebar_context)
            elif re.match(r"^/users/\d+", pathname):
                user_id = re.match(r"^/users/(\d+)", pathname).group(1)
                db = SessionLocal()
                try:
                    user = CRUDUser.get(db, id=user_id)
                finally:
                    db.close()
                if user:
                    return views.users_update.layout(sidebar_context, user)
                else:
                    return views.error.layout(sidebar_context)
        return views.error.layout(sidebar_context)
    else:
        return views.login.layout(sidebar_context)


@app.callback(Output("urlRefresh", "href"), [Input("navigationLogout", "n_clicks")])
def logout(n_clicks):
    if n_clicks is None:
        raise PreventUpdate()
    logout_user()
    return "/"
