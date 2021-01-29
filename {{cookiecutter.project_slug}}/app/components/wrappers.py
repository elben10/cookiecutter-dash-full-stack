import dash_html_components as html
from app.components.navigation import navigation
from app.components.sidebar import sidebar


def main_wrapper(element, sidebar_context):
    return html.Div(
        [
            sidebar(sidebar_context),
            html.Div(
                [
                    navigation(),
                    html.Div(
                        element,
                        className="container-fluid flex-grow-1 d-flex flex-column",
                    ),
                ],
                id="content-wrapper",
                className="d-flex flex-column",
            ),
        ],
        id="wrapper",
    )
