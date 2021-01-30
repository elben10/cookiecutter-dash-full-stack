# flake8: noqa E501

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pydantic import ValidationError

from app.app import app
from app.components.cards import grid_card
from app.components.notification import notification
from app.components.wrappers import main_wrapper
from app.crud import CRUDUser
from app.db.session import SessionLocal
from app.schemas import UserCreate
from app.schemas.utils import get_error_message
from app.utils import triggered_by_id


def layout(sidebar_context):
    title = html.H1("Create User", className="h3 text-gray-800 mb-4")
    form_notification = notification("userCreateFormNotification")
    form = [
        html.Div(
            [
                html.Label(
                    "Full Name",
                    className="small mb-1",
                    htmlFor="usersCreateFullname",
                ),
                dcc.Input(
                    className="form-control",
                    id="usersCreateFullname",
                    placeholder="Enter your full name...",
                ),
            ],
            className="form-group",
        ),
        html.Div(
            [
                html.Label(
                    "Email",
                    className="small mb-1",
                    htmlFor="usersCreateEmail",
                ),
                dcc.Input(
                    type="email",
                    className="form-control",
                    id="usersCreateEmail",
                    placeholder="Enter Email Address...",
                    value="",
                ),
                html.Div(
                    id="usersCreateEmailValidation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="form-group",
        ),
        html.Div(
            [
                html.Label(
                    "Password",
                    className="small mb-1",
                    htmlFor="usersCreatePassword",
                ),
                dcc.Input(
                    className="form-control",
                    placeholder="New password",
                    type="password",
                    id="usersCreatePassword",
                    value="",
                ),
                html.Div(
                    id="usersCreatePasswordValidation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="form-group",
        ),
        html.Div(
            [
                html.Label(
                    "Repeat Password",
                    className="small mb-1",
                    htmlFor="usersCreatePassword2",
                ),
                dcc.Input(
                    className="form-control",
                    placeholder="Repeat new password",
                    type="password",
                    id="usersCreatePassword2",
                    value="",
                ),
                html.Div(
                    id="usersCreatePassword2Validation",
                    className="invalid-feedback d-flex",
                ),
            ],
            className="form-group",
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
                value=["IsActive"],
                inputClassName="mr-2",
                labelClassName="mr-3",
                id="usersCreateCheckboxes",
            ),
            className="form-group",
        ),
        html.Button("Save", className="btn btn-primary", id="usersCreateSave"),
    ]
    form_container = html.Div(
        html.Div(
            grid_card("User Information", form),
            className="col-xl-6 col-lg-12",
        ),
        className="row",
    )
    return main_wrapper([title, form_notification, form_container], sidebar_context)


@app.callback(
    [
        Output("userCreateFormNotification", "className"),
        Output("userCreateFormNotificationHeaderContainer", "className"),
        Output("userCreateFormNotificationHeader", "children"),
        Output("userCreateFormNotificationBody", "children"),
        Output("usersCreateFullname", "value"),
        Output("usersCreateEmail", "value"),
        Output("usersCreatePassword", "value"),
        Output("usersCreatePassword2", "value"),
        Output("usersCreateCheckboxes", "value"),
        Output("usersCreateEmailValidation", "children"),
        Output("usersCreatePasswordValidation", "children"),
        Output("usersCreatePassword2Validation", "children"),
    ],
    [
        Input("usersCreateSave", "n_clicks"),
        Input("userCreateFormNotificationClose", "n_clicks"),
    ],
    [
        State("usersCreateFullname", "value"),
        State("usersCreateEmail", "value"),
        State("usersCreatePassword", "value"),
        State("usersCreatePassword2", "value"),
        State("usersCreateCheckboxes", "value"),
    ],
    prevent_initial_call=True,
)
def create_user(_, __, full_name, email, password, password2, check_list):
    noti_class = "toast-header bg-primary text-white"
    if triggered_by_id(
        dash.callback_context.triggered, "userCreateFormNotificationClose"
    ):
        return (
            "toast",
            noti_class,
            None,
            None,
            full_name,
            email,
            password,
            password2,
            check_list,
            None,
            None,
            None,
        )
    try:
        user_in = UserCreate(
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
            "toast",
            noti_class,
            None,
            None,
            full_name,
            email,
            password,
            password2,
            check_list,
            get_error_message(errors, "email"),
            get_error_message(errors, "password"),
            get_error_message(errors, "password2"),
        )
    except Exception:
        return (
            "toast show",
            "toast-header bg-danger text-white",
            "Error",
            "An unexpected Error happened try to reload the page, and try again",
            full_name,
            email,
            password,
            password2,
            check_list,
            None,
            None,
            None,
        )

    db = SessionLocal()
    try:
        user = CRUDUser.get_by_email(db, email=email)
        if user:
            return (
                "toast",
                noti_class,
                None,
                None,
                full_name,
                email,
                password,
                password2,
                check_list,
                "User already exists",
                None,
                None,
            )
        CRUDUser.create(db, user_in=user_in)
    finally:
        db.close()

    return (
        "toast show",
        "toast-header bg-success text-white",
        "Success",
        "The user was succesfully created",
        "",
        "",
        "",
        "",
        ["IsActive"],
        None,
        None,
        None,
    )
