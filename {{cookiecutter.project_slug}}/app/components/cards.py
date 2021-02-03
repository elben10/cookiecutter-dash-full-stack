# flake8: noqa E501
import dash_core_components as dcc
import dash_html_components as html
from dash_core_components.Tab import Tab
from dash_core_components.Tabs import Tabs


def card(key, value, icon, color="primary"):
    return html.Div(
        html.Div(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                key,
                                className=f"text-xs font-weight-bold text-{color} text-uppercase mb-1",
                            ),
                            html.Div(
                                value,
                                className="h5 mb-0 font-weight-bold text-gray-800",
                            ),
                        ],
                        className="col mr-2",
                    ),
                    html.Div(html.I(className=icon), className="col-auto"),
                ],
                className="row no-gutters align-items-center",
            ),
            className="card-body",
        ),
        className=f"card border-left-{color} shadow h-100 py-2",
    )


def grid_card(title, element, dropdown_options=None):
    return html.Div(
        [
            html.Div(
                [
                    html.H6(title, className="m-0 font-weight-bold text-primary"),
                    html.Div(
                        [
                            html.Div(
                                html.I(
                                    className="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"
                                ),
                                className="dropdown-toggle",
                                role="button",
                                id="dropdownMenuLink",
                                **{
                                    "data-toggle": "dropdown",
                                    "aria-haspopup": "true",
                                    "aria-expanded": "false",
                                },
                            ),
                            html.Div(
                                dropdown_options,
                                className="dropdown-menu dropdown-menu-right shadow animated--fade-in",
                                **{"aria-labelledby": "dropdownMenuLink"},
                            ),
                        ],
                        className="dropdown no-arrow",
                    )
                    if dropdown_options
                    else None,
                ],
                className="card-header py-3 d-flex flex-row align-items-center justify-content-between",
            ),
            html.Div(element, className="card-body"),
        ],
        className="card shadow mb-4 h-100",
    )


def tab_card(element, id, elements, value=None):
    return html.Div(
        [
            dcc.Tabs(
                [
                    dcc.Tab(
                        label=element["label"],
                        value=element["value"],
                        className="tab-card",
                        selected_className="tab-card-enabled",
                        disabled_className="tab-card-disabled",
                    )
                    for element in elements
                ],
                id=id,
                value=value,
            ),
            html.Div(element, className="card-body", id=f"{id}Body"),
        ],
        className="card shadow mb-4 h-100",
        style={"overflow": "hidden"},
    )
