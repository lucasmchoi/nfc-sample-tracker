# -*- coding: utf-8 -*-
"""
Created on Monday, 2024-06-17 22:02

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
import sys
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


uid_salt = os.getenv("USERS_UID_SALT", "horrible salt")
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")
gui_username = os.getenv("MONGO_GUI_USER", "nfc-gui-user")
gui_password = os.getenv("MONGO_GUI_PASSWORD")
database = os.getenv("MONGO_DATABASE", "nfc-tracking")

#############################################################
database = "nfc-example"
gui_password = "mP5hWvlECX_14_dHPq7csFp3Pf4cFgH7idC6SVv3_yiaTYCLupN75mev8B2M87E-lUwhiKIjN9x0N8F14D86Lg"
#############################################################

client = MongoClient(
    f"mongodb://{gui_username}:{gui_password}@{mongo_host}:{mongo_port}/{database}"
)

db = client[database]

# case for testing
if len(sys.argv) > 2 and sys.argv[2] == "testing":
    GITCWD = None
    URLBASEPATH = None
    # __tmpdir__ = None
    # pathnameadd = ""
    # pathnamecut = 0
    DEBUGB = True
else:
    GITCWD = "/raid/syncthing/git-webhook/nfc-sample-tracker/"
    URLBASEPATH = "/nst/"
    # __tmpdir__ = "/raid/messdaten-temp/"  # tmpdir for import tempfile if necessary
    # pathnameadd = "/raid/messdaten/"
    # pathnamecut = len(urlbasepath)
    DEBUGB = False

# get version and short hash
# __version__ = check_output(
#     ["git", "describe", "--abbrev=0", "--tags"], text=True, cwd=GITCWD
# ).strip()
__shorthash__ = check_output(
    ["git", "rev-parse", "--short", "HEAD"], text=True, cwd=GITCWD
).strip()

# set dash_bootstrap_components stylesheet
external_stylesheets = [dbc.themes.CERULEAN]

app = Dash(
    __name__,
    url_base_pathname=URLBASEPATH,
    external_stylesheets=external_stylesheets,
    serve_locally=True,
)


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
    # add path for teraaxel
    memory["fpath"] = pathname
    memory["version"] = {"hash": __shorthash__}
    return memory


if __name__ == "__main__":
    # adds debugging mode when testing
    app.run(debug=DEBUGB, port=int(sys.argv[1]))
