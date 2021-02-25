# flake8: noqa E501

import re

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
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
from app.utils import triggered_by_id


def layout(sidebar_context, user):
    title = html.H1("Update User", className="h3 text-gray-800 mb-4")
    form_notification = notification("usersUpdateFormNotification")
    location = dcc.Location("userUpdateUrlRefresh", refresh=True)
    form = [
        html.Div(
            [
                html.Label(
                    "Full Name",
                    className="small mb-1",
                    htmlFor="usersUpdateFullname",
                ),
                dcc.Input(
                    className="form-control",
                    id="usersUpdateFullname",
                    placeholder="Enter your full name...",
                    value=user.full_name,
                ),
            ],
            className="mb-2",
        ),
        html.Div(
            [
                html.Label(
                    "Email",
                    className="small mb-1",
                    htmlFor="usersUpdateEmail",
                ),
                dcc.Input(
                    type="email",
                    className="form-control",
                    id="usersUpdateEmail",
                    placeholder="Enter Email Address...",
                    value=user.email,
                ),
                html.Div(
                    id="usersUpdateEmailValidation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="mb-2",
        ),
        html.Div(
            [
                html.Label(
                    "Password",
                    className="small mb-1",
                    htmlFor="usersUpdatePassword",
                ),
                dcc.Input(
                    className="form-control",
                    placeholder="New password",
                    type="password",
                    id="usersUpdatePassword",
                    value="",
                ),
                html.Div(
                    id="usersUpdatePasswordValidation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="mb-2",
        ),
        html.Div(
            [
                html.Label(
                    "Repeat Password",
                    className="small mb-1",
                    htmlFor="usersUpdatePassword2",
                ),
                dcc.Input(
                    className="form-control",
                    placeholder="Repeat new password",
                    type="password",
                    id="usersUpdatePassword2",
                    value="",
                ),
                html.Div(
                    id="usersUpdatePassword2Validation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="mb-2",
        ),
        html.Div(
            dcc.Checklist(
                options=[
                    {
                        "label": "Is Active",
                        "value": "IsActive",
                    },
                    {
                        "label": "Is Superuser",
                        "value": "IsSuperuser",
                    },
                ],
                value=(["IsActive"] if user.is_active else [])
                + (["IsSuperuser"] if user.is_superuser else []),
                inputClassName="me-2",
                labelClassName="me-3",
                id="usersUpdateCheckboxes",
            ),
            className="mb-2",
        ),
        html.Div(
            [
                html.Button(
                    "Save", className="btn btn-primary me-2", id="usersUpdateSave"
                ),
                html.Button(
                    "Delete", className="btn btn-danger me-2 text-white", id="usersUpdateDelete"
                ),
            ],
            className="d-flex",
        ),
    ]
    form_container = html.Div(
        html.Div(
            grid_card("User Information", form),
            className="col-xl-6 col-lg-12",
        ),
        className="row",
    )
    return main_wrapper(
        [title, location, form_notification, form_container], sidebar_context
    )


@app.callback(
    [
        Output("userUpdateUrlRefresh", "href"),
        Output("usersUpdateFormNotification", "className"),
        Output("usersUpdateFormNotificationHeaderContainer", "className"),
        Output("usersUpdateFormNotificationHeader", "children"),
        Output("usersUpdateFormNotificationBody", "children"),
        Output("usersUpdateEmailValidation", "children"),
        Output("usersUpdatePasswordValidation", "children"),
        Output("usersUpdatePassword2Validation", "children"),
        Output("usersUpdatePassword", "value"),
        Output("usersUpdatePassword2", "value"),
    ],
    [
        Input("usersUpdateSave", "n_clicks"),
        Input("usersUpdateDelete", "n_clicks"),
        Input("usersUpdateFormNotificationClose", "n_clicks"),
    ],
    [
        State("urlNoRefresh", "pathname"),
        State("usersUpdateFullname", "value"),
        State("usersUpdateEmail", "value"),
        State("usersUpdatePassword", "value"),
        State("usersUpdatePassword2", "value"),
        State("usersUpdateCheckboxes", "value"),
    ],
    prevent_initial_call=True,
)
def update_user(
    _, __, ___, pathname, full_name, email, password, password2, check_list
):
    if not current_user.is_superuser:
        raise PreventUpdate()
    noti_class = "toast-header bg-primary text-white"
    user_id = re.match(r"^/users/(\d+)", pathname).group(1)
    if triggered_by_id(
        dash.callback_context.triggered, "usersUpdateFormNotificationClose"
    ):
        return (
            None,
            "toast",
            noti_class,
            None,
            None,
            None,
            None,
            None,
            password,
            password2,
        )

    if triggered_by_id(dash.callback_context.triggered, "usersUpdateDelete"):
        db = SessionLocal()
        try:
            CRUDUser.delete(db, id=user_id)
        finally:
            db.close()
        return (
            "/",
            "toast",
            noti_class,
            None,
            None,
            None,
            None,
            None,
            password,
            password2,
        )

    try:
        user_in = UserUpdate(
            full_name=full_name,
            email=email,
            password=password,
            password2=password2,
            is_active="IsActive" in check_list,
            is_superuser="IsSuperuser" in check_list,
        )
    except ValidationError as e:
        errors = e.errors()
        return (
            None,
            "toast show",
            noti_class,
            None,
            None,
            get_error_message(errors, "email"),
            get_error_message(errors, "password"),
            get_error_message(errors, "password2"),
            password,
            password2,
        )

    db = SessionLocal()
    try:
        user = CRUDUser.get(db, id=user_id)
        CRUDUser.update(db, user=user, user_in=user_in)
    finally:
        db.close()
    return (
        None,
        "toast show",
        "toast-header bg-success text-white",
        "Success",
        "User successfully updated",
        None,
        None,
        None,
        "",
        "",
    )
