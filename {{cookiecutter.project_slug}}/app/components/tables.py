# flake8: noqa E501

import math

import dash_core_components as dcc
import dash_html_components as html


def table(
    id,
    column_definitions,
    table_sizes=[10, 20, 50],
):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        html.Div(
                            html.Div(
                                [
                                    "Show ",
                                    dcc.Dropdown(
                                        style={
                                            "display": "inline-block",
                                            "verticalAlign": "middle",
                                        },
                                        options=[
                                            {"label": str(i), "value": i}
                                            for i in table_sizes
                                        ],
                                        value=table_sizes[0],
                                        id=f"{id}TableSize",
                                    ),
                                    " entries",
                                ],
                                className="dataTables_length",
                            ),
                            className="col-sm-12 col-md-6",
                        ),
                        className="row",
                    ),
                    html.Div(
                        html.Div(
                            html.Table(
                                [
                                    html.Thead(
                                        html.Tr(
                                            [
                                                html.Th(
                                                    [column["title"]],
                                                    className="bg-primary text-white"
                                                    + (
                                                        " sorting"
                                                        if column.get("sortable")
                                                        else ""
                                                    ),
                                                    id={
                                                        "type": f"{id}ColumnHeader",
                                                        "index": idx,
                                                    },
                                                    style={
                                                        "position": "sticky",
                                                        "top": 0,
                                                    },
                                                )
                                                for idx, column in enumerate(
                                                    column_definitions
                                                )
                                            ]
                                        )
                                    ),
                                    html.Tbody(id=f"{id}Body"),
                                ],
                                className="table table-striped table-bordered dataTable no-footer",
                            ),
                            className="col-sm-12",
                            style={"overflow-y": "scroll", "maxHeight": "70vh"},
                        ),
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Div(
                                html.Div(
                                    "Showing 0 to 0 of 0 entries",
                                    id=f"{id}EntriesText",
                                    className="dataTables_info",
                                ),
                                className="col-sm-12 col-md-5",
                            ),
                            html.Div(
                                html.Div(
                                    html.Ul(
                                        [
                                            html.Li(
                                                dcc.Link(
                                                    "Previous",
                                                    href="#",
                                                    className="page-link",
                                                ),
                                                className="paginate_button page-item previous disabled",
                                            ),
                                            html.Li(
                                                dcc.Link(
                                                    "1",
                                                    href="#",
                                                    className="page-link",
                                                    style={"cursor": "auto"},
                                                ),
                                                className="paginate_button page-item active",
                                            ),
                                            html.Li(
                                                dcc.Link(
                                                    "Next",
                                                    href="#",
                                                    className="page-link",
                                                ),
                                                className="paginate_button page-item next disabled",
                                            ),
                                        ],
                                        className="pagination",
                                        id=f"{id}Pagination",
                                    ),
                                    className="dataTables_paginate paging_simple_numbers dataTables_info",
                                ),
                                className="col-sm-12 col-md-7",
                            ),
                        ],
                        className="row",
                    ),
                ],
                className="dataTables_wrapper dt-bootstrap4",
            ),
            dcc.Store(data={"page": 1}, id=f"{id}PageStore"),
        ],
        className="table-responsive",
    )


def generate_entries_text(page, table_size, n_rows):
    from_text, to_text = ((page - 1) * table_size) + 1, min((page) * table_size, n_rows)
    return f"Showing {from_text} to {to_text} of {n_rows} entries"


def calculate_number_of_pages(n_items, page_size):
    return math.ceil(n_items / page_size)


def calculate_start_end_total(current_page, n_items, page_size):
    total_pages = calculate_number_of_pages(n_items, page_size)
    if total_pages <= 5:
        return 1, total_pages, total_pages
    else:
        if current_page <= 3:
            return 1, 5, total_pages
        elif current_page + 1 >= total_pages:
            return total_pages - 4, total_pages, total_pages
        else:
            if (total_pages - (current_page - 2)) == 5:
                return current_page - 1, current_page + 3, total_pages
            else:
                return current_page - 2, current_page + 2, total_pages


def generate_pagination(id, current_page, n_items, page_size):
    start_page, end_page, total_pages = calculate_start_end_total(
        current_page, n_items, page_size
    )
    res = []
    if current_page == 1:
        res.append(
            html.Li(
                html.Div(
                    "Previous",
                    className="page-link",
                ),
                className="paginate_button page-item previous disabled",
                id={"type": f"{id}ItemPagination", "index": 0},
            )
        )
    else:
        res.append(
            html.Li(
                html.Div(
                    "Previous",
                    className="page-link",
                    style={"cursor": "pointer"},
                ),
                className="paginate_button page-item previous",
                id={"type": f"{id}ItemPagination", "index": 0},
            )
        )

    for page in range(start_page, end_page + 1):
        res.append(
            html.Li(
                html.Div(
                    page,
                    className="page-link",
                    style={"cursor": "pointer"} if page != current_page else None,
                ),
                className="paginate_button page-item"
                + (" active" if page == current_page else ""),
                id={"type": f"{id}ItemPagination", "index": page},
            )
        )

    if current_page == total_pages:
        res.append(
            html.Li(
                html.Div(
                    "Next",
                    className="page-link",
                ),
                className="paginate_button page-item previous disabled",
                id={"type": f"{id}ItemPagination", "index": total_pages + 1},
            )
        )
    else:
        res.append(
            html.Li(
                html.Div(
                    "Next",
                    style={"cursor": "pointer"},
                    className="page-link",
                ),
                className="paginate_button page-item previous",
                id={"type": f"{id}ItemPagination", "index": total_pages + 1},
            )
        )
    return res
