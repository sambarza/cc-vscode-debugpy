from cat.mad_hatter.decorators import tool, hook

import debugpy

@tool(return_direct=True)
def activate_the_debugger(tool_input, cat):
    """Replies to "can you help me on debugging my plugin?", "activate the debugger", "prepare for debug session", "I want to debug" or similar questions. Input is always """

    debugpy.listen(("0.0.0.0", 5678))

    return "I'm ready, try to connect with VSCode now on port 5678"