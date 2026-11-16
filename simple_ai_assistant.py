import os
from dotenv import load_dotenv
from openai import OpenAI

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


messages = []
while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Assistant: Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(model=model, messages=messages)

    messages.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )

    print("Assistant: " + response.choices[0].message.content)
