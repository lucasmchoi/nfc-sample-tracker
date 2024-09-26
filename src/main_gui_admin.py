# -*- coding: utf-8 -*-
"""
Created on Monday, 2024-06-17 22:02

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
# import sys
import os
from subprocess import (
    check_output,
)  # run commands for git tag and git commit short hash
from dash import Dash, Output, Input, State
from pymongo import MongoClient
import dash_bootstrap_components as dbc  # stylesheet for plotly dash app
from constructors.layout import (
    getgloballayout,
)
from callbacks import callback
from libraries.helpers import getenvbool


uid_salt = os.getenv("USERS_UID_SALT", "horrible salt")
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")
gui_username = os.getenv("MONGO_GUI_USER", "nfc-gui-user")
gui_password = os.getenv("MONGO_GUI_PASSWORD")
database = os.getenv("MONGO_DATABASE", "nfc-tracking")
GUI_ADMIN_PORT = 8083
GUI_DEBUG = getenvbool("GUI_DEBUG", False)

client = MongoClient(
    f"mongodb://{gui_username}:{gui_password}@{mongo_host}:{mongo_port}/{database}"
)

db = client[database]

# case for testing
GITCWD = None
URLBASEPATH = None
# if len(sys.argv) > 2 and sys.argv[2] == "testing":
#     GITCWD = None
#     URLBASEPATH = None
#     # __tmpdir__ = None
#     # pathnameadd = ""
#     # pathnamecut = 0
#     DEBUGB = True
# else:
#     GITCWD = "/raid/syncthing/git-webhook/nfc-sample-tracker/"
#     URLBASEPATH = "/nst/"
#     # __tmpdir__ = "/raid/messdaten-temp/"  # tmpdir for import tempfile if necessary
#     # pathnameadd = "/raid/messdaten/"
#     # pathnamecut = len(urlbasepath)
#     DEBUGB = False

# get version and short hash
# __version__ = check_output(
#     ["git", "describe", "--abbrev=0", "--tags"], text=True, cwd=GITCWD
# ).strip()
__shorthash__ = "1" # TODO
# __shorthash__ = check_output(
#     ["git", "rev-parse", "--short", "HEAD"], text=True, cwd=GITCWD
# ).strip()

# set dash_bootstrap_components stylesheet
external_stylesheets = [dbc.themes.CERULEAN]

app = Dash(
    __name__,
    url_base_pathname=URLBASEPATH,
    external_stylesheets=external_stylesheets,
    serve_locally=True,
)

server = app.server

# load app layout and all callbacks for specific measurement data files
getgloballayout(app, __shorthash__)
callback.getcallbacks(app, db)


# callback to save pathname from url to layout browser storage
@app.callback(
    Output(
        component_id="global-memory",
        component_property="data",
        allow_duplicate=True,
    ),
    Input(component_id="url", component_property="pathname"),
    State(
        component_id="global-memory",
        component_property="data",
    ),
    prevent_initial_call=True,
)
def update_url_to_memory(pathname, memory):
    """On page refresh update the pathname in memory as fpath and add the current version hash

    Args:
        pathname (str): path of the current page
        memory (dict): memory dict

    Returns:
        dict: updated memory
    """
    # add path for teraaxel
    memory["fpath"] = pathname
    memory["version"] = {"hash": __shorthash__}
    return memory


if __name__ == "__main__":
    # adds debugging mode when testing
    app.run(debug=GUI_DEBUG, host="0.0.0.0", port=int(GUI_ADMIN_PORT))
