# flake8: noqa E501

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from dash_data_table import DashDataTable

from app.app import app
from app.components.wrappers import main_wrapper
from app.crud import CRUDUser
from app.db.session import SessionLocal
from app.utils import get_trigger_id, get_trigger_index

column_definitions = [
    {"name": "ID", "selector": "id"},
    {"name": "Full Name", "selector": "full_name"},
    {"name": "Email", "selector": "email"},
    {"name": "Is Active", "selector": "is_active", "type": "checkbox"},
    {"name": "Is Superuser", "selector": "is_superuser", "type": "checkbox"},
    {"name": "Update User", "selector": "update_user", "type": "button"},
]


def layout(sidebar_context):
    title_row = html.Div(
        [
            html.H1("Users", className="h3 mb-0 text-gray-800"),
            dcc.Link(
                [html.I(className="fa fa-plus pr-2"), "Create User"],
                className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm",
                href="/users/create",
            ),
        ],
        className="d-sm-flex align-items-center justify-content-between mb-4",
    )
    return main_wrapper(
        [
            title_row,
            DashDataTable(
                id="usersTable",
                columns=column_definitions,
                persistTableHead=True,
                paginationServer=True,
            ),
        ],
        sidebar_context,
    )


@app.callback(
    Output("usersTable", "data"),
    Output("usersTable", "paginationTotalRows"),
    Input("usersTable", "currentPage"),
    Input("usersTable", "currentRowsPerPage"),
)
def update_table(page, rows_per_page):
    page = page if page else 1
    rows_per_page = rows_per_page if rows_per_page else 10
    db = SessionLocal()
    try:
        users = CRUDUser.get_multi(
            db, limit=rows_per_page, skip=(page - 1) * rows_per_page
        )
        n_rows = CRUDUser.count(db)
        return [
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "update_user": {"href": f"/users/{user.id}", "text": "Update User"},
            }
            for user in users
        ], n_rows
    finally:
        db.close()
