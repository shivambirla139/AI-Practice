import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, run_tool
from Utility.utilities import log

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
MAX_STEPS = 10



messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Keep your responses concise. Use available tools when appropriate.",
    }
]

while True:
    user_input = input("\n🧑 You: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("🤖 Assistant: Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    for step in range(MAX_STEPS):
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
            print("🤖 Assistant: " + assistant_reply)
            break

        log(f"  Step {step + 1}: model requested {len(message.tool_calls)} tool calls")
        messages.append({"role": "assistant", "tool_calls": message.tool_calls})

        for tool_call in message.tool_calls:
            tool_result = run_tool(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )
    else:
        print("🤖 Assistant: Reached maximum number of steps without completing the request.")
