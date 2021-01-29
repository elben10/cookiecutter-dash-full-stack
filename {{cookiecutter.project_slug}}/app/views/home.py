import dash_core_components as dcc
import dash_html_components as html

from app.components.cards import card, grid_card
from app.components.tables import table
from app.components.wrappers import main_wrapper


def layout(sidebar_context):
    title = html.H1("Dashboard", className="h3 text-gray-800 mb-4")
    card_row = html.Div(
        [
            html.Div(
                card(
                    "Earnings (Monthly)",
                    "$40,000",
                    "fas fa-calendar fa-2x text-gray-300",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card(
                    "Earnings (Monthly)",
                    "$40,000",
                    "fas fa-calendar fa-2x text-gray-300",
                    "secondary",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card(
                    "Earnings (Monthly)",
                    "$40,000",
                    "fas fa-calendar fa-2x text-gray-300",
                    "warning",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card(
                    "Earnings (Monthly)",
                    "$40,000",
                    "fas fa-calendar fa-2x text-gray-300",
                    "danger",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
        ],
        className="row",
    )

    graph_row = html.Div(
        [
            html.Div(
                grid_card(
                    "Graph",
                    dcc.Graph(
                        figure={
                            "layout": {"margin": {"t": 10, "l": 20, "r": 20, "b": 20}},
                            "data": [
                                {
                                    "uid": "45c0a4",
                                    "line": {
                                        "color": "rgb(255, 127, 14)",
                                        "shape": "spline",
                                        "width": 3,
                                    },
                                    "mode": "lines",
                                    "name": "iOS & Android",
                                    "type": "scatter",
                                    "x": [
                                        "2007-12-01",
                                        "2008-12-01",
                                        "2009-12-01",
                                        "2010-12-01",
                                        "2011-12-01",
                                        "2012-12-01",
                                        "2013-12-01",
                                        "2014-12-01",
                                        "2015-12-01",
                                    ],
                                    "y": [
                                        "0",
                                        "45560506.663365364",
                                        "91145081.21192169",
                                        "232447635.15836716",
                                        "580348915.5698586",
                                        "1182888421.2842617",
                                        "1928559640.2194986",
                                        "2578825762.2643065",
                                        "3022276546.8773637",
                                    ],
                                }
                            ],
                        },
                        className="h-100",
                        style={"minHeight": "250px"},
                        responsive=True,
                    ),
                ),
                className="col-12 col-md-6 pt-2 pb-4",
            )
        ]
        * 2,
        className="row flex-grow-1",
    )

    return main_wrapper(
        [title, card_row, graph_row, graph_row],
        sidebar_context,
    )
