import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, get_current_time

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
        "content": "You are a helpful assistant. Keep your responses concise. Only call the get_current_time tool when the user asks for the current date or time.",
    }
]

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Assistant: Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
        tool_choice=TOOL_CHOICE,
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]

        if tool_call.function.name == "get_current_time":
            time_result = get_current_time()
            messages.append({"role": "assistant", "tool_calls": message.tool_calls})
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": time_result,
                }
            )

            final_response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=TOOLS,
                tool_choice=TOOL_CHOICE,
            )
            final_text = final_response.choices[0].message.content or "I don't know."
            messages.append({"role": "assistant", "content": final_text})
            print("Assistant: " + final_text)
        else:
            print("Assistant: I can't do that.")
        continue

    assistant_reply = message.content or "I don't know."
    messages.append({"role": "assistant", "content": assistant_reply})
    print("Assistant: " + assistant_reply)
