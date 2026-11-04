"""Adds "Diorama (editable)", a dashboard in storage mode holding a copy of
config/diorama.yaml, so the card's editor can be tried on the demo flat.

Runs before Home Assistant on every start of the container. The dashboard is
added when it is missing, and its copy of the flat is written only when there
is none yet, so edits made in the UI are kept. Delete
config/.storage/lovelace.diorama_editable and restart to start again from
the current diorama.yaml.
"""

import json
import os

import yaml

STORAGE = "/config/.storage"
ID = "diorama_editable"


def read(name, default):
    try:
        with open(os.path.join(STORAGE, name)) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def write(name, data):
    with open(os.path.join(STORAGE, name), "w") as f:
        json.dump(data, f, indent=2)


dashboards = read(
    "lovelace_dashboards",
    {"version": 1, "minor_version": 1, "key": "lovelace_dashboards", "data": {"items": []}},
)
if not any(item["id"] == ID for item in dashboards["data"]["items"]):
    dashboards["data"]["items"].append(
        {
            "id": ID,
            "url_path": "diorama-editable",
            "title": "Diorama (editable)",
            "icon": "mdi:floor-plan",
            "show_in_sidebar": True,
            "require_admin": False,
            "mode": "storage",
        }
    )
    write("lovelace_dashboards", dashboards)

key = f"lovelace.{ID}"
if read(key, None) is None:
    with open("/config/diorama.yaml") as f:
        config = yaml.safe_load(f)
    write(key, {"version": 1, "minor_version": 1, "key": key, "data": {"config": config}})
