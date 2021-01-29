import dash_html_components as html


def notification(id):
    return html.Div(
        html.Div(
            [
                html.Div(
                    [
                        html.I(className="fas fa-exclamation-circle mr-2"),
                        html.Span(id=f"{id}Header", className="mr-auto"),
                        html.Button(
                            "x", className="ml-2 mb-1 close text-white", id=f"{id}Close"
                        ),
                    ],
                    className="toast-header bg-primary text-white",
                    id=f"{id}HeaderContainer"
                ),
                html.Div(
                    id=f"{id}Body",
                    className="toast-body",
                ),
            ],
            id=id,
            className="toast",
            role="alert",
            **{"aria-live": "assertive", "aria-atomic": "true", "data-delay": "5000"},
        ),
        style={
            "position": "fixed",
            "bottom": "1rem",
            "right": "1rem",
            "zIndex": "1000",
        },
    )
