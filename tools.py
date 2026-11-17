from datetime import datetime
import requests


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
    }
]


FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
}

