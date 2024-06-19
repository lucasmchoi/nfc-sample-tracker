# -*- coding: utf-8 -*-
"""
Created on Tuesday, 2024-06-18 20:37

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from dash import dash_table, html
import pandas as pd


def get_users(db):
    projection = {
        "_id": 1,
        "name": {"$concat": ["$name.last", ", ", "$name.first"]},
        "email": 1,
        "userid": 1,
    }
    data = db["users"].find({}, projection)
    ldata = []

    for entry in data:
        pipeline = [
            {"$match": {"responsible-user": entry["_id"]}},
            {"$count": "total_count"},
        ]

        samples_responsibility = list(db["samples"].aggregate(pipeline))[0][
            "total_count"
        ]

        entry["email"] = "[{}](mailto:{}?subject=NFC%20sample%20tracker)".format(
            entry["email"], entry["email"]
        )

        entry["samples"] = "[{}](/users/{})".format(
            samples_responsibility, entry["_id"]
        )
        entry["_id"] = str(entry["_id"])
        ldata.append(entry)

    df = pd.DataFrame(ldata)
    return html.Div(
        [
            html.Div([html.H2("Users")]),
            html.Div(
                [
                    dash_table.DataTable(
                        data=df.to_dict("records"),
                        columns=[
                            {"name": "name", "id": "name", "presentation": "markdown"},
                            {
                                "name": "email",
                                "id": "email",
                                "presentation": "markdown",
                            },
                            {
                                "name": "samples",
                                "id": "samples",
                                "presentation": "markdown",
                            },
                            {
                                "name": "userid",
                                "id": "userid",
                                "presentation": "markdown",
                            },
                            {"name": "_id", "id": "_id", "presentation": "markdown"},
                        ],
                        style_cell={
                            "whiteSpace": "normal",
                            "height": "auto",
                            "maxWidth": 0,
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "textAlign": "center",
                        },
                        css=[dict(selector="p", rule="margin: 0; text-align: center")],
                        markdown_options={"link_target": "_self"},
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                    ),
                ]
            ),
        ]
    )
