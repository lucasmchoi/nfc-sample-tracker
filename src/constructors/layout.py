# -*- coding: utf-8 -*-
"""
Created on Monday, 2024-06-17 23:13

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
from dash import html, dcc  # plotly dash layout elements
import dash_bootstrap_components as dbc  # bootstrap layout elements


def getgloballayout(app, __shorthash__):
    """sets the layout for the app

    Args:
        app (dash app): dash app
        __version__ (string): version number
        __shorthash__ (string): short git commit hash
    """

    # App layout
    app.layout = dbc.Container(
        [
            dcc.Store(id="global-memory", data={}),
            # set header line
            dbc.Row(
                [
                    dbc.NavbarSimple(
                        children=[
                            dbc.NavItem(dbc.NavLink("Users", href="/users")),
                            dbc.NavItem(dbc.NavLink("Locations", href="/locations")),
                            dbc.NavItem(dbc.NavLink("Samples", href="/samples")),
                            dbc.NavItem(dbc.NavLink("Add User", href="/adduser")),
                            dbc.NavItem(
                                dbc.NavLink("Add Location", href="/addlocation")
                            ),
                        ],
                        brand=f"NFC sample tracker - ({__shorthash__})",
                        brand_href="/",
                        color="primary",
                        dark=True,
                        style={"width": "100%", "display": "inline-block"},
                    ),
                    # url path memory
                    dcc.Location(id="url"),
                ]
            ),
            dbc.Container(
                [
                    dbc.Form(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="text",
                                                    id="add-location-form-name",
                                                ),
                                                dbc.Label("Location name"),
                                            ]
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="text",
                                                    id="add-location-form-room",
                                                ),
                                                dbc.Label("Room"),
                                            ]
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "Submit",
                                            color="primary",
                                            id="add-locaton-form-submit",
                                        ),
                                        width="auto",
                                    ),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="text",
                                                    id="add-location-form-street",
                                                ),
                                                dbc.Label("Street"),
                                            ]
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="text",
                                                    id="add-location-form-zip",
                                                ),
                                                dbc.Label("ZIP"),
                                            ]
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="text",
                                                    id="add-location-form-city",
                                                ),
                                                dbc.Label("City"),
                                            ]
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="text",
                                                    id="add-location-form-country",
                                                ),
                                                dbc.Label("Country"),
                                            ]
                                        )
                                    ),
                                ]
                            ),
                        ],
                        style={"display": "none"},
                        id="location-form",
                    ),
                    dbc.Form(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="text",
                                                    id="add-user-form-first-name",
                                                ),
                                                dbc.Label("First name"),
                                            ]
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="text",
                                                    id="add-user-form-last-name",
                                                ),
                                                dbc.Label("Last name"),
                                            ]
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(
                                                    type="email",
                                                    id="add-user-form-email",
                                                ),
                                                dbc.Label("E-Mail"),
                                            ]
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "Submit",
                                            color="primary",
                                            id="add-user-form-submit",
                                        ),
                                        width="auto",
                                    ),
                                ]
                            ),
                        ],
                        style={"display": "none"},
                        id="user-form",
                    ),
                    html.Div(
                        id="data-view",
                    ),
                ]
            ),
        ],
        fluid=True,
    )
