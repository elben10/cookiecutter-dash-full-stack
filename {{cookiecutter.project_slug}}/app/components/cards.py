# flake8: noqa E501

import dash_html_components as html


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
