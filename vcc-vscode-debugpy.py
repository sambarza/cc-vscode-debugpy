from cat.mad_hatter.decorators import tool, hook

import os
import json
from pydantic import BaseModel

import debugpy

# This is the fixed port exposed in docker-compose.yml
LISTENING_PORT = 5678


class MySettings(BaseModel):
    # Should be `bool` not `str`, waiting for the fix ;-)
    listen_on_bootstrap: str = "NO"


@hook
def plugin_settings_schema():
    return MySettings.schema()


@hook
def before_cat_bootstrap(cat):
    settings = load_settings()

    if "listen_on_bootstrap" in settings and settings["listen_on_bootstrap"] == "YES":
        try:
            start_listening()
        except Exception as e:
            # Investigate how to use the Cat logging system
            print(f"{e}")


@tool(return_direct=True)
def activate_the_debugger(tool_input, cat):
    """Replies to "can you help me on debugging my plugin?", "activate the debugger", "prepare for debug session", "I want to debug" or similar questions. Input is always None"""

    try:
        start_listening()
    except Exception as e:
        return f"{e}"

    return f"I'm ready, you can connect with VSCode on port {LISTENING_PORT}"


def start_listening():
    """Start listening for incoming debug sessions from vscode"""

    print(f"Listening for debug sessions on port {LISTENING_PORT}")
    debugpy.listen(("0.0.0.0", LISTENING_PORT))


def load_settings():
    """This is copy and paste of the core method `Plugin.load_settings()`
    Investigate how to reuse the core method...
    """

    path = "cat/plugins/cc-vscode-debugpy/"

    # by default, plugin settings are saved inside the plugin folder
    #   in a JSON file called settings.json
    settings_file_path = os.path.join(path, "settings.json")

    # default settings is an empty dictionary
    settings = {}

    # load settings.json if exists
    if os.path.isfile(settings_file_path):
        try:
            with open(settings_file_path, "r") as json_file:
                settings = json.load(json_file)
        except Exception as e:
            print(f"Unable to load plugin cc-vscode-debugpy settings", "ERROR")
            print(e, "ERROR")

    return settings
