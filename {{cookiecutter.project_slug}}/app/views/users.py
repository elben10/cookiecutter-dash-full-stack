import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from app.app import app
from app.components.wrappers import main_wrapper
from app.components.tables import (
    calculate_number_of_pages,
    table,
    generate_entries_text,
    generate_pagination,
)
from app.crud import CRUDUser
from app.db.session import SessionLocal
from app.utils import get_trigger_id, get_trigger_index


column_definitions = [
    {"title": "ID"},
    {"title": "Full Name"},
    {"title": "Email"},
    {"title": "Is Active"},
    {"title": "Is Superuser"},
    {"title": "Update User"},
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
    table_ = table("users", column_definitions)
    return main_wrapper(
        [title_row, table_],
        sidebar_context,
    )


@app.callback(
    [
        Output("usersBody", "children"),
        Output("usersEntriesText", "children"),
        Output("usersPagination", "children"),
        Output("usersPageStore", "data"),
    ],
    [
        Input("usersTableSize", "value"),
        Input({"type": "usersItemPagination", "index": ALL}, "n_clicks"),
    ],
    [State("usersPageStore", "data")],
)
def update_table(value, _, page_store):
    db = SessionLocal()

    try:
        users = CRUDUser.get_multi(db, limit=value)
        n_rows = CRUDUser.count(db)
        if get_trigger_id(dash.callback_context.triggered) == "usersItemPagination":
            index = get_trigger_index(dash.callback_context.triggered)
            total_pages = calculate_number_of_pages(n_rows, value)
            if index == page_store["page"]:
                raise PreventUpdate()
            elif index == 0 and page_store["page"] == 1:
                raise PreventUpdate()
            elif index == total_pages + 1 and page_store["page"] == total_pages:
                raise PreventUpdate()
            elif index == 0 and page_store["page"] > 1:
                page_store["page"] -= 1
            elif index == total_pages + 1 and page_store["page"] < total_pages:
                page_store["page"] += 1
            elif index > 0 and index < total_pages + 1:
                page_store["page"] = index

        return (
            [
                html.Tr(
                    [
                        html.Td(row.id, className="align-middle"),
                        html.Td(row.full_name, className="align-middle"),
                        html.Td(row.email, className="align-middle"),
                        html.Td(str(row.is_active), className="align-middle"),
                        html.Td(str(row.is_superuser), className="align-middle"),
                        html.Td(
                            dcc.Link(
                                html.Button("Update User", className="btn btn-primary"),
                                href=f"/users/{row.id}",
                            ),
                            className="text-center",
                        ),
                    ],
                    className="even" if idx % 2 == 0 else "odd",
                )
                for idx, row in enumerate(users)
            ],
            generate_entries_text(page_store["page"], value, n_rows),
            generate_pagination("users", page_store["page"], n_rows, value),
            page_store,
        )
    finally:
        db.close()