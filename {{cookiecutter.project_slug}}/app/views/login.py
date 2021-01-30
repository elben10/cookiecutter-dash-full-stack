# flake8: noqa E501

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import login_user

from app.app import app
from app.crud import CRUDUser
from app.db.session import SessionLocal


def layout(sidebar_context):
    return [
        dcc.Location(id="loginRefresher", refresh=True),
        html.Div(
            html.Div(
                html.Div(
                    html.Div(
                        html.Div(
                            html.Div(
                                html.Div(
                                    [
                                        html.Div(
                                            className="col-lg-6 d-none d-lg-block bg-login-image"
                                        ),
                                        html.Div(
                                            html.Div(
                                                [
                                                    html.Div(
                                                        html.H1(
                                                            "Welcome Back",
                                                            className="h4 text-gray-900 mb-4",
                                                        ),
                                                        className="text-center",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                    dcc.Input(
                                                                        type="email",
                                                                        className="form-control form-control-user",
                                                                        id="loginUsername",
                                                                        placeholder="Enter Email Address...",
                                                                    ),
                                                                    html.Div(
                                                                        id="loginUsernameValidation",
                                                                        className="invalid-feedback d-block",
                                                                    ),
                                                                ],
                                                                className="form-group",
                                                            ),
                                                            html.Div(
                                                                [
                                                                    dcc.Input(
                                                                        type="password",
                                                                        className="form-control form-control-user",
                                                                        id="loginPassword",
                                                                        placeholder="Password",
                                                                    ),
                                                                    html.Div(
                                                                        id="loginPasswordValidation",
                                                                        className="invalid-feedback d-block",
                                                                    ),
                                                                ],
                                                                className="form-group",
                                                            ),
                                                            html.Div(
                                                                html.Div(
                                                                    dcc.Checklist(
                                                                        id="loginRememberMe",
                                                                        options=[
                                                                            {
                                                                                "label": "Remember Me",
                                                                                "value": True,
                                                                            },
                                                                        ],
                                                                        labelClassName="align-bottom",
                                                                        inputClassName="mr-2 align-middle",
                                                                        value=[True],
                                                                    ),
                                                                    className="custom-checkbox small",
                                                                ),
                                                                className="form-group",
                                                            ),
                                                            html.Button(
                                                                "Login",
                                                                className="btn btn-primary btn-user btn-block",
                                                                id="loginSubmit",
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                dcc.Link(
                                                                    "Forgot Password",
                                                                    href="/",
                                                                    className="small",
                                                                ),
                                                                className="text-center",
                                                            ),
                                                        ],
                                                        className="user",
                                                    ),
                                                ],
                                                className="p-5",
                                            ),
                                            className="col-lg-6",
                                        ),
                                    ],
                                    className="row",
                                    style={"min-height": "500px"},
                                ),
                                className="card-body p-0",
                            ),
                            className="card o-hidden border-0 shadow-lg my-5",
                        ),
                        className="col-xl-10 col-lg-12 col-md-9",
                    ),
                    className="row justify-content-center",
                ),
                className="container",
            ),
            className="bg-gradient-primary",
            style={"minHeight": "100vh"},
        ),
    ]


@app.callback(
    Output("loginRefresher", "href"),
    [Input("loginSubmit", "n_clicks")],
    [State("loginUsername", "value"), State("loginPassword", "value")],
)
def login(n_clicks, email, password):
    if n_clicks is None:
        raise PreventUpdate()
    db = SessionLocal()
    try:
        user = CRUDUser.authenticate(db, email=email, password=password)
        if user:
            login_user(user)
            return "/"
    finally:
        db.close()
