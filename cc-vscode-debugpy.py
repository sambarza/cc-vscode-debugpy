from cat.mad_hatter.decorators import tool, hook, plugin

from cat.log import log
from pydantic import BaseModel, Field


import debugpy

# This is the fixed port exposed in docker-compose.yml
LISTENING_PORT = 5678

# Plugin name, used to load settings
PLUGIN_NAME = "cc_vscode_debugpy"


class MySettings(BaseModel):
    listen_on_bootstrap: bool = Field(
        default=False,
        title="Start listening for debug sessions during bootstrap",
    )
    debug_bootstrap: bool = Field(
        default=False,
        title="Stop the Cat bootstrap (useful to debug the bootstrap process)",
    )


@plugin
def settings_schema():
    return MySettings.schema()


@hook
def before_cat_bootstrap(cat):
    settings = cat.mad_hatter.plugins[PLUGIN_NAME].load_settings()

    if listen_on_bootstrap(settings) or debug_bootstrap(settings):
        try:
            start_listening()
        except Exception as e:
            # Investigate how to use the Cat logging system
            print(f"{e}")

    if debug_bootstrap(settings):
        try:
            wait_for_client()
        except Exception as e:
            # Investigate how to use the Cat logging system
            print(f"{e}")


def listen_on_bootstrap(settings):
    return "listen_on_bootstrap" in settings and settings["listen_on_bootstrap"]


def debug_bootstrap(settings):
    return "debug_bootstrap" in settings and settings["debug_bootstrap"]


@tool(return_direct=True)
def activate_the_debugger(tool_input, cat):
    """Replies to "can you help me on debugging my plugin?", "activate the debugger", "prepare for debug session", "I want to debug" or similar questions. Input is always None"""

    try:
        start_listening()
    except Exception as e:
        return f"{e}"

    return f"I'm ready, you can connect with VSCode on port {LISTENING_PORT}, remember to open the port in docker-compose.yml"


def start_listening():
    """Start listening for incoming debug sessions from vscode"""

    print(f"Listening for debug sessions on port {LISTENING_PORT}")

    debugpy.listen(("0.0.0.0", LISTENING_PORT))


def wait_for_client():
    """Wait for a client connection, this is blocking"""

    log(
        f"Waiting for debug sessions on port {LISTENING_PORT}, attach with VSCode to continue startup",
        "WARNING",
    )
    debugpy.wait_for_client()


@tool(return_direct=True)
def activate_breakpoint(tool_input, cat):
    """Replies to "set breakpoint" or similar questions. Input is always None"""

    debugpy.breakpoint()

    return f"Ok breakpoint set"
