import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("api_key")
base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("BASE_URL")
model = os.getenv("OPENAI_MODEL") or os.getenv("model") or "gpt-4o-mini"

if not api_key:
    raise ValueError(
        "Missing API key. Set OPENAI_API_KEY or api_key in your .env file."
    )

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

TOOL_CHOICE = "auto"



messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Keep your responses concise. Use available tools when appropriate.",
    }
]

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Assistant: Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice=TOOL_CHOICE,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            assistant_reply = message.content or "I don't know."
            messages.append({"role": "assistant", "content": assistant_reply})
            print("Assistant: " + assistant_reply)
            break

        messages.append({"role": "assistant", "tool_calls": message.tool_calls})

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = FUNCTION_NAME_TO_FUNCTION_MAP.get(function_name)

            if function_to_call:
                args = (
                    json.loads(tool_call.function.arguments)
                    if tool_call.function.arguments
                    else {}
                )
                try:
                    tool_result = function_to_call(**args)
                except TypeError:
                    tool_result = function_to_call()

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(tool_result),
                    }
                )
            else:
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"Error: Tool '{function_name}' is not recognized.",
                    }
                )
