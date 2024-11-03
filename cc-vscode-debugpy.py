import socket

from cat.mad_hatter.decorators import tool, hook, plugin

from cat.log import log
from pydantic import BaseModel, Field


import debugpy

# This is the fixed port exposed in docker-compose.yml
LISTENING_PORT = 5678


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
    settings = cat.mad_hatter.get_plugin().load_settings()

    if listen_on_bootstrap(settings) or debug_bootstrap(settings):
        try:
            start_listening()
            if not is_debug_port_exposed():
                log.error(f"The port {LISTENING_PORT} doesn't seem to be exposed in the `compose.yml` file. You need to expose it")

        except Exception as e:
            log.error(f"{e}")

    if debug_bootstrap(settings):
        try:
            if not is_debug_port_exposed():
                log.warning(f"The port {LISTENING_PORT} doesn't seem to be exposed in the `compose.yml` file. Startup has not stopped")
            else:
                wait_for_client()

        except Exception as e:
            log.error(f"{e}")


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

    if not is_debug_port_exposed():
        return f"I'm ready, however the port {LISTENING_PORT} doesn't seem to be exposed in the `compose.yml` file. You need to expose it"

    return f"I'm ready, you can connect with VSCode on port {LISTENING_PORT}"

@tool(return_direct=True)
def tool_is_debug_port_exposed(tool_input, cat):
    """Replies to "is the debug port exposed?"""

    if not is_debug_port_exposed():
        return f"The debug port {LISTENING_PORT} seems to be exposed"
    else:
        return f"The debug port {LISTENING_PORT} doesn't seem to be exposed"

def start_listening():
    """Start listening for incoming debug sessions from vscode"""

    log.info(f"Listening for debug sessions on port {LISTENING_PORT}")
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

def is_debug_port_exposed():

    return is_port_open(f"host.docker.internal", LISTENING_PORT)

def is_port_open(host, port, timeout=0.250):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout)

    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        return False
    except socket.gaierror:
        # Host name not resolved, probably we are not running in Docker
        # We assume you know what you're doing and hope the port is open
        return True

    try:
        # Receive the connection messages
        # If the connection is interrupted before receiving these messages,
        # the debug server get stuck and stop handling new connections.
        while client_socket.recv(256):
            pass

        # should never go here

    except TimeoutError:
        # It's fine to timeout after receiving connection messages
        return True
    except socket.error as e:
        # Other errors? Consider the port closed
        log.error(e.strerror)
        return False
    finally:
        client_socket.close()