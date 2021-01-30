# flake8: noqa E501

import dash_core_components as dcc
import dash_html_components as html
from flask_login import current_user


def sidebar(sidebar_context):
    return html.Ul(
        [
            logo_item(),
            html.Hr(className="sidebar-divider my-0"),
            *(
                [
                    sidebar_item(elem["title"], elem["icon"], elem["href"])
                    for elem in sidebar_context
                ]
            ),
            *(
                [
                    html.Div("Admin", className="sidebar-heading"),
                    sidebar_item("Users", "fas fa-user fa-sm fa-fw", "/users"),
                ]
                if current_user.is_superuser
                else []
            ),
            html.Hr(className="sidebar-divider d-none d-md-block"),
            html.Div(
                html.Button(className="rounded-circle border-0", id="sidebarToggle"),
                className="text-center d-none d-md-inline",
            ),
        ],
        className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion",
    )


def logo_item():
    return dcc.Link(
        [
            html.Div(
                html.I(className="fas fa-laugh-wink"),
                className="sidebar-brand-icon rotate-n-15",
            ),
            html.Div("SB Admin", className="sidebar-brand-text mx-3"),
        ],
        className="sidebar-brand d-flex align-items-center justify-content-center",
        href="/",
    )


def sidebar_item(title, icon, href, active=False):
    class_name = "nav-item" + (" active" if active else "")
    return html.Li(
        dcc.Link(
            [html.I(className=icon), html.Span(title)],
            className="nav-link",
            href=href,
        ),
        className=class_name,
    )
