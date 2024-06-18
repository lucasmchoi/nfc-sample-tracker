# -*- coding: utf-8 -*-
"""
Created on Monday, 2024-06-17 23:13

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
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
            dbc.Container(html.Div(id="data-view")),
        ],
        fluid=True,
    )
