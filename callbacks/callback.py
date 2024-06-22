# -*- coding: utf-8 -*-
"""
Created on Monday, 2024-06-17 23:13

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from dash import Output, Input, no_update
from dash.exceptions import PreventUpdate
from constructors.helpers import check_menu_selection
from callbacks.users import get_users
from callbacks.user import get_user
from callbacks.locations import get_locations
from callbacks.location import get_location
from callbacks.samples import get_samples
from callbacks.newlocation import get_location_callbacks


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
        Input(component_id="global-memory", component_property="data"),
        prevent_initial_call=True,
    )
    def update_data(memory):
        fpath = memory["fpath"]
        if check_menu_selection(fpath, "", 1):
            return None, {"display": "none"}
        elif check_menu_selection(fpath, "users", 1):
            return get_users(db), {"display": "none"}
        elif check_menu_selection(fpath, "user", 2):
            return get_user(db, fpath.split("/")[2]), {"display": "none"}
        elif check_menu_selection(fpath, "locations", 1):
            return get_locations(db), {"display": "none"}
        elif check_menu_selection(fpath, "location", 2):
            return get_location(db, fpath.split("/")[2]), {"display": "none"}
        elif check_menu_selection(fpath, "samples", 1):
            return get_samples(db), {"display": "none"}
        elif check_menu_selection(fpath, "addlocation", 1):
            return None, {"display": "block"}
        else:
            raise PreventUpdate
        
    get_location_callbacks(app, db)
