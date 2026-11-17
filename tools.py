from datetime import datetime


def get_current_time():
    """
    Returns the current local date and time in a readable format.
    """
    return datetime.now().strftime("%A, %d %B %Y at %I:%M %p")


# This tools list is meant to be passed to the LLM in chat.completions.create(..., tools=tools)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local date and time in a readable format.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

