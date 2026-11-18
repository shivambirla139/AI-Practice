from datetime import datetime
import json
import requests
from Utilities.utilities import log


def get_current_time():
    """
    Returns the current local date and time in a readable format.
    """
    return datetime.now().strftime("%A, %d %B %Y at %I:%M %p")


def get_city_weather(city_name):
    """
    Gets the current weather for a given city using wttr.in.
    """
    try:
        response = requests.get(f"https://wttr.in/{city_name}?format=3", timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        return f"Error: Unable to fetch weather (status code: {response.status_code})"
    except Exception as e:
        return f"Error fetching weather: {e}"


def get_current_city():
    """
    Returns the user's current city or location.
    """
    return "bangalore"


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
    },
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": "Get the current weather for a specified city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "The name of the city to get the weather for (e.g., 'Paris', 'Tokyo', 'London')."
                    }
                },
                "required": ["city_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_city",
            "description": "Get the user's currently lived-in city or location. Use this when the user asks about 'my location', 'my city', 'my place', or where they currently live.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_current_city": get_current_city,
}


def run_tool(tool_call) -> str:
    """
    Executes a tool call from the model, logs the execution details,
    and returns the result as a string.
    """
    function_name = tool_call.function.name
    function_to_call = FUNCTION_NAME_TO_FUNCTION_MAP.get(function_name)

    if not function_to_call:
        error_msg = f"Tool '{function_name}' is not recognized."
        log(f"      Error: {error_msg}")
        return f"Error: {error_msg}"

    try:
        args = (
            json.loads(tool_call.function.arguments)
            if tool_call.function.arguments
            else {}
        )
        log(f"    🔧 {function_name}({args})")
        try:
            tool_result = function_to_call(**args)
        except TypeError:
            tool_result = function_to_call()
        log(f"      ↳ {tool_result}")
        return str(tool_result)
    except Exception as e:
        error_msg = f"Failed to execute function '{function_name}': {e}"
        log(f"      Error: {error_msg}")
        return f"Error: {error_msg}"


