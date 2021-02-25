# flake8: noqa E501

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_login import current_user
from pydantic import ValidationError

from app.app import app
from app.components.cards import grid_card
from app.components.notification import notification
from app.components.wrappers import main_wrapper
from app.crud import CRUDUser
from app.db.session import SessionLocal
from app.schemas import UserUpdate
from app.schemas.utils import get_error_message
from app.security import verify_password
from app.utils import triggered_by_id


def layout(sidebar_context):
    title = html.H1("Profile", className="h3 text-gray-800 mb-4")
    account_notification = notification("usersProfileAccountNotification")
    account_form = [
        html.Div(
            [
                html.Label(
                    "Email",
                    className="small mb-1",
                    htmlFor="usersProfileEmail",
                ),
                dcc.Input(
                    type="email",
                    className="form-control",
                    id="usersProfileEmail",
                    placeholder="Enter Email Address...",
                    value=current_user.email,
                    disabled=True,
                ),
            ],
            className="mb-2",
        ),
        html.Div(
            [
                html.Label(
                    "Full Name",
                    className="small mb-1",
                    htmlFor="usersProfileFullname",
                ),
                dcc.Input(
                    className="form-control",
                    id="usersProfileFullname",
                    placeholder="Enter your full name...",
                    value=current_user.full_name,
                ),
            ],
            className="mb-2",
        ),
        html.Div(
            dcc.Checklist(
                options=[
                    {
                        "label": "Is Active",
                        "value": current_user.is_active,
                        "disabled": True,
                    },
                    {
                        "label": "Is Superuser",
                        "value": current_user.is_superuser,
                        "disabled": True,
                    },
                ],
                value=[True],
                inputClassName="me-2",
                labelClassName="me-2",
            ),
            className="mb-2",
        ),
        html.Button("Save", className="btn btn-primary", id="usersProfileSave"),
    ]
    account_form_container = html.Div(
        html.Div(
            grid_card("Profile information", account_form),
            className="col-xl-6 col-lg-12 pb-3",
        ),
        className="row",
    )

    password_notification = notification("usersProfilePasswordNotification")
    password_form = [
        html.Div(
            [
                html.Label(
                    "Old Password",
                    className="small mb-1",
                    htmlFor="usersProfileOldPassword",
                ),
                dcc.Input(
                    className="form-control",
                    placeholder="Old password",
                    type="password",
                    id="usersProfileOldPassword",
                ),
                html.Div(
                    id="usersProfileOldPasswordValidation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="mb-2",
        ),
        html.Div(
            [
                html.Label(
                    "New Password",
                    className="small mb-1",
                    htmlFor="usersProfileNewPassword",
                ),
                dcc.Input(
                    className="form-control",
                    placeholder="New password",
                    type="password",
                    id="usersProfileNewPassword",
                ),
                html.Div(
                    id="usersProfileNewPasswordValidation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="mb-2",
        ),
        html.Div(
            [
                html.Label(
                    "Repeat New Password",
                    className="small mb-1",
                    htmlFor="usersProfileNewPassword2",
                ),
                dcc.Input(
                    className="form-control",
                    placeholder="Repeat new password",
                    type="password",
                    id="usersProfileNewPassword2",
                ),
                html.Div(
                    id="usersProfileNewPassword2Validation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="mb-2",
        ),
        html.Button("Save", className="btn btn-primary", id="usersProfilePasswordSave"),
    ]
    password_form_container = html.Div(
        html.Div(
            grid_card("Update Password", password_form),
            className="col-xl-6 col-lg-12",
        ),
        className="row",
    )
    return main_wrapper(
        [
            title,
            account_notification,
            account_form_container,
            password_notification,
            password_form_container,
        ],
        sidebar_context,
    )


@app.callback(
    [
        Output("usersProfileAccountNotification", "className"),
        Output("usersProfileAccountNotificationHeaderContainer", "className"),
        Output("usersProfileAccountNotificationHeader", "children"),
        Output("usersProfileAccountNotificationBody", "children"),
    ],
    [
        Input("usersProfileSave", "n_clicks"),
        Input("usersProfileAccountNotificationClose", "n_clicks"),
    ],
    [
        State("usersProfileFullname", "value"),
    ],
    prevent_initial_call=True,
)
def update_profile_information(n_clicks_save, _, full_name):
    if triggered_by_id(
        dash.callback_context.triggered, "usersProfileAccountNotificationClose"
    ):
        return "toast", "toast-header bg-primary text-white", None, None
    db = SessionLocal()
    try:
        user_in = UserUpdate(full_name=full_name)
        CRUDUser.update(db, user=current_user, user_in=user_in)
    finally:
        db.close()

    return (
        "toast show",
        "toast-header bg-success text-white",
        "Success",
        "The user was succesfully updated",
    )


@app.callback(
    [
        Output("usersProfilePasswordNotification", "className"),
        Output("usersProfilePasswordNotificationHeaderContainer", "className"),
        Output("usersProfilePasswordNotificationHeader", "children"),
        Output("usersProfilePasswordNotificationBody", "children"),
        Output("usersProfileOldPasswordValidation", "children"),
        Output("usersProfileNewPasswordValidation", "children"),
        Output("usersProfileNewPassword2Validation", "children"),
        Output("usersProfileOldPassword", "value"),
        Output("usersProfileNewPassword", "value"),
        Output("usersProfileNewPassword2", "value"),
    ],
    [
        Input("usersProfilePasswordSave", "n_clicks"),
        Input("usersProfilePasswordNotificationClose", "n_clicks"),
    ],
    [
        State("usersProfileOldPassword", "value"),
        State("usersProfileNewPassword", "value"),
        State("usersProfileNewPassword2", "value"),
    ],
    prevent_initial_call=True,
)
def update_password(n_clicks_save, _, old_password, password, password2):
    noti_class = "toast-header bg-primary text-white"
    if triggered_by_id(
        dash.callback_context.triggered, "usersProfilePasswordNotificationClose"
    ):
        return "toast", noti_class, None, None, None, None, None, "", "", ""
    if not verify_password(old_password or "", current_user.hashed_password):
        return (
            "toast",
            noti_class,
            None,
            None,
            "Couldn't validate old password",
            None,
            None,
            old_password,
            password,
            password2,
        )

    if not password:
        return (
            "toast",
            noti_class,
            None,
            None,
            None,
            "Value is required",
            None,
            old_password,
            password,
            password2,
        )

    try:
        user_in = UserUpdate(password=password, password2=password2)
    except ValidationError as e:
        errors = e.errors()
        return (
            "toast",
            noti_class,
            None,
            None,
            None,
            get_error_message(errors, "password"),
            get_error_message(errors, "password2"),
            old_password,
            password,
            password2,
        )

    db = SessionLocal()
    try:
        CRUDUser.update(db, user=current_user, user_in=user_in)
    finally:
        db.close()

    return (
        "toast show",
        "toast-header bg-success text-white",
        "Success",
        "The user was succesfully updated",
        None,
        None,
        None,
        "",
        "",
        "",
    )
