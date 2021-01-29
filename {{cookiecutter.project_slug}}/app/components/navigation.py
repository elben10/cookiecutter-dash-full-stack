import dash_core_components as dcc
import dash_html_components as html
from flask_login import current_user

def navigation():
    return html.Nav(
        [
            html.Button(
                html.I(className="fa fa-bars"),
                id="sidebarToggleTop",
                className="btn btn-link d-md-none rounded-circle mr-3",
            ),
            html.Ul(
                [
                    html.Div(className="topbar-divider d-none d-sm-block"),
                    html.Li(
                        [
                            html.A(
                                [
                                    html.Span(
                                        current_user.full_name if current_user.full_name else current_user.email,
                                        className="mr-2 d-none d-lg-inline text-gray-600 small",
                                    ),
                                    html.I(className="fas fa-user d-lg-none d-inline"),
                                ],
                                className="nav-link dropdown-toggle",
                                href="#",
                                id="userDropdown",
                                role="button",
                                **{
                                    "data-toggle": "dropdown",
                                    "aria-haspopup": "true",
                                    "aria-expanded": "false",
                                },
                            ),
                            html.Div(
                                [
                                    dcc.Link(
                                        [
                                            html.I(
                                                className="fas fa-user fa-sm fa-fw mr-2 text-gray-400"
                                            ),
                                            "Profile",
                                        ],
                                        href="/users/profile",
                                        className="dropdown-item",
                                    ),
                                    html.Div(className="dropdown-divider"),
                                    html.Button(
                                        [
                                            html.I(
                                                className="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"
                                            ),
                                            "Logout",
                                        ],
                                        className="dropdown-item",
                                        id="navigationLogout",
                                    ),
                                ],
                                className="dropdown-menu dropdown-menu-right shadow animated--grow-in",
                                **{"aria-labelledby": "userDropdown"},
                            ),
                        ],
                        className="nav-item dropdown no-arrow",
                    ),
                ],
                className="navbar-nav ml-auto",
            ),
        ],
        className="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow",
    )