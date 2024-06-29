# -*- coding: utf-8 -*-
"""
Created on Saturday, 2024-06-22 10:03

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright ©  2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
from dash import dash_table, html
import pandas as pd


def get_samples(db):
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "sample-number": 1,
                "material": "$information.material",
                "orientation": "$information.orientation",
                "doping": "$information.doping",
                "growth": "$information.growth",
                "responsible-user": 1,
                "current_location": {
                    "$arrayElemAt": [
                        {
                            "$slice": [
                                {
                                    "$sortArray": {
                                        "input": "$locations",
                                        "sortBy": {"date": -1},
                                    }
                                },
                                1,
                            ]
                        },
                        0,
                    ]
                },
            }
        },
        {
            "$project": {
                "sample-number": 1,
                "material": 1,
                "orientation": 1,
                "doping": 1,
                "growth": 1,
                "current_location": "$current_location.location",
                "responsible-user": 1,
            }
        },
    ]

    samples = list(db["samples"].aggregate(pipeline))

    for entry in samples:
        projection = {
            "_id": 1,
            "name": {"$concat": ["$name.first", " ", "$name.last"]},
        }

        responsible_user = db["users"].find_one(
            {"_id": entry["responsible-user"]}, projection
        )

        entry["responsible-user"] = "[{}](/user/{})".format(
            responsible_user["name"], responsible_user["_id"]
        )

        location = db["locations"].find_one(
            {"_id": entry["current_location"]}, {"_id": 0, "name": 1}
        )

        entry["current_location"] = "[{}](/location/{})".format(
            location["name"], entry["current_location"]
        )

    df = pd.DataFrame(samples)

    return html.Div(
        [
            html.Div([html.H2("Samples")]),
            html.Div(
                [
                    dash_table.DataTable(
                        data=df.to_dict("records"),
                        columns=[
                            {
                                "name": "sample number",
                                "id": "sample-number",
                                "presentation": "markdown",
                            },
                            {
                                "name": "current location",
                                "id": "current_location",
                                "presentation": "markdown",
                            },
                            {
                                "name": "material",
                                "id": "material",
                                "presentation": "markdown",
                            },
                            {
                                "name": "orientation",
                                "id": "orientation",
                                "presentation": "markdown",
                            },
                            {
                                "name": "growth",
                                "id": "growth",
                                "presentation": "markdown",
                            },
                            {
                                "name": "growth",
                                "id": "growth",
                                "presentation": "markdown",
                            },
                            {
                                "name": "responsibility",
                                "id": "responsible-user",
                                "presentation": "markdown",
                            },
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
