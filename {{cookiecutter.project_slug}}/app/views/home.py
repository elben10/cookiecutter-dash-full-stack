# flake8: noqa E501
from time import sleep

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app.app import app
from app.components.cards import card, grid_card, tab_card
from app.components.wrappers import main_wrapper

GRAPH_LAYOUT = {"margin": {"t": 10, "l": 20, "r": 20, "b": 20}}


def layout(sidebar_context):
    title = html.H1("Dashboard", className="h3 text-gray-800 mb-4")
    card_row = html.Div(
        [
            html.Div(
                card(
                    "Earnings (Monthly)",
                    "fas fa-calendar fa-2x text-gray-300",
                    id="firstCard",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card(
                    "Earnings (Monthly)",
                    "fas fa-calendar fa-2x text-gray-300",
                    color="secondary",
                    id="secondCard",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card(
                    "Earnings (Monthly)",
                    "fas fa-calendar fa-2x text-gray-300",
                    color="warning",
                    id="thirdCard",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card(
                    "Earnings (Monthly)",
                    "fas fa-calendar fa-2x text-gray-300",
                    color="danger",
                    id="forthCard",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
        ],
        className="row",
    )

    graph_row1 = html.Div(
        [
            html.Div(
                grid_card(
                    "Graph",
                    dcc.Graph(
                        id="graph1",
                        figure={"layout": GRAPH_LAYOUT, "data": []},
                        className="h-100",
                        style={"minHeight": "100px"},
                        responsive=True,
                    ),
                ),
                className="col-12 col-md-6 pt-2 pb-4",
            ),
            html.Div(
                tab_card(
                    None,
                    id="tab1",
                    elements=[
                        {"label": "Option 1", "value": "0"},
                        {"label": "Option 2", "value": "1"},
                        {"label": "Option 3", "value": "2"},
                    ],
                    value="0",
                ),
                className="col-12 col-md-6 pt-2 pb-4",
            ),
        ],
        className="row flex-grow-1",
    )

    graph_row2 = html.Div(
        [
            html.Div(
                grid_card(
                    "Graph",
                    dcc.Graph(
                        id="graph2",
                        figure={"layout": GRAPH_LAYOUT, "data": []},
                        className="h-100",
                        style={"minHeight": "100px"},
                        responsive=True,
                    ),
                ),
                className="col-12 col-md-6 pt-2 pb-4",
            ),
            html.Div(
                tab_card(
                    None,
                    id="tab2",
                    elements=[
                        {"label": "Option 1", "value": "0"},
                        {"label": "Option 2", "value": "1"},
                        {"label": "Option 3", "value": "2"},
                    ],
                    value="0",
                ),
                className="col-12 col-md-6 pt-2 pb-4",
            ),
        ],
        className="row flex-grow-1",
    )

    return main_wrapper(
        [title, card_row, graph_row1, graph_row2],
        sidebar_context,
    )


@app.callback(
    [
        Output("firstCard", "children"),
        Output("secondCard", "children"),
        Output("thirdCard", "children"),
        Output("forthCard", "children"),
    ],
    [Input("urlNoRefresh", "href")],
)
def load_cards(_):
    return "$40,000", "$40,000", "$40,000", "$40,000"


@app.callback(Output("graph1", "figure"), [Input("urlNoRefresh", "href")])
def update_figure1(_):
    sleep(3)
    return {
        "layout": GRAPH_LAYOUT,
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
    }


@app.callback(Output("graph2", "figure"), [Input("urlNoRefresh", "href")])
def update_figure2(_):
    return {
        "layout": GRAPH_LAYOUT,
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
    }


@app.callback(
    Output("tab1Body", "children"),
    [Input("urlNoRefresh", "href"), Input("tab1", "value")],
)
def update_tab1(_, tabValue):
    if tabValue == "0":
        return dcc.Graph(
            figure={
                "layout": GRAPH_LAYOUT,
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
            style={"minHeight": "100px"},
            responsive=True,
        )
    elif tabValue == "1":
        return dcc.Graph(
            figure={
                "layout": GRAPH_LAYOUT,
                "data": [
                    {
                        "uid": "45c0a4",
                        "line": {
                            "color": "red",
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
            style={"minHeight": "100px"},
            responsive=True,
        )
    elif tabValue == "2":
        return dcc.Graph(
            figure={
                "layout": GRAPH_LAYOUT,
                "data": [
                    {
                        "uid": "45c0a4",
                        "line": {
                            "color": "green",
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
            style={"minHeight": "100px"},
            responsive=True,
        )


@app.callback(
    Output("tab2Body", "children"),
    [Input("urlNoRefresh", "href"), Input("tab2", "value")],
)
def update_tab1(_, tabValue):
    sleep(3)
    if tabValue == "0":
        return dcc.Graph(
            figure={
                "layout": GRAPH_LAYOUT,
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
            style={"minHeight": "100px"},
            responsive=True,
        )
    elif tabValue == "1":
        return dcc.Graph(
            figure={
                "layout": GRAPH_LAYOUT,
                "data": [
                    {
                        "uid": "45c0a4",
                        "line": {
                            "color": "red",
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
            style={"minHeight": "100px"},
            responsive=True,
        )
    elif tabValue == "2":
        return dcc.Graph(
            figure={
                "layout": GRAPH_LAYOUT,
                "data": [
                    {
                        "uid": "45c0a4",
                        "line": {
                            "color": "green",
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
            style={"minHeight": "100px"},
            responsive=True,
        )
