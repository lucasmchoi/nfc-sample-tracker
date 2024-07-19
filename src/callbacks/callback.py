# -*- coding: utf-8 -*-
"""
Created on Monday, 2024-06-17 23:13

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
from dash import Output, Input, no_update
from dash.exceptions import PreventUpdate
from constructors.helpers import check_menu_selection
from callbacks.users import get_users
from callbacks.user import get_user
from callbacks.locations import get_locations
from callbacks.location import get_location
from callbacks.samples import get_samples
from callbacks.newlocation import get_newlocation_callbacks
from callbacks.newuser import get_newuser_callbacks


def getcallbacks(app, db):
    @app.callback(
        Output(
            component_id="data-view",
            component_property="children",
            allow_duplicate=True,
        ),
        Output(
            component_id="location-form",
            component_property="style",
            allow_duplicate=True,
        ),
        Output(
            component_id="user-form",
            component_property="style",
            allow_duplicate=True,
        ),
        Input(component_id="global-memory", component_property="data"),
        prevent_initial_call=True,
    )
    def update_data(memory):
        fpath = memory["fpath"]
        nodp = {"display": "none"}
        bdp = {"display": "block"}
        if check_menu_selection(fpath, "", 1):
            return None, nodp, nodp
        elif check_menu_selection(fpath, "users", 1):
            return get_users(db), nodp, nodp
        elif check_menu_selection(fpath, "user", 2):
            return get_user(db, fpath.split("/")[2]), nodp, nodp
        elif check_menu_selection(fpath, "locations", 1):
            return get_locations(db), nodp, nodp
        elif check_menu_selection(fpath, "location", 2):
            return get_location(db, fpath.split("/")[2]), nodp, nodp
        elif check_menu_selection(fpath, "samples", 1):
            return get_samples(db), nodp, nodp
        elif check_menu_selection(fpath, "addlocation", 1):
            return None, bdp, nodp
        elif check_menu_selection(fpath, "adduser", 1):
            return None, nodp, bdp
        else:
            raise PreventUpdate

    get_newlocation_callbacks(app, db)
    get_newuser_callbacks(app, db)
