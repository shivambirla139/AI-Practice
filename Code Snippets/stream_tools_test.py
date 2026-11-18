# standard library imports
import os
import sys
from pathlib import Path
from types import SimpleNamespace

# Add project root to sys.path so top-level modules like tools.py can be found
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Third-party imports
from openai import OpenAI
from dotenv import load_dotenv

# Local modules
from tools import TOOLS

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

stream = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[{"role": "user", "content": "What is the weather in Pune ?"}],
    tools=TOOLS,
    stream=True,
)

calls = {}   # index -> tool call being built

for chunk in stream:
    if not chunk.choices:                       # some servers send chunks with no choices
        continue
    delta = chunk.choices[0].delta

    for tc in (delta.tool_calls or []):
        obj = calls.setdefault(
            tc.index,
            SimpleNamespace(id=None, function=SimpleNamespace(name="", arguments="")),
        )
        if tc.id:
            obj.id = tc.id
        if tc.function and tc.function.name:
            obj.function.name += tc.function.name
        if tc.function and tc.function.arguments:
            obj.function.arguments += tc.function.arguments

calls_list = []
for key in sorted(calls):
    calls_list.append(calls[key])

print("Reconstructed Tool Calls:")
for call in calls_list:
    print(f"ID: {call.id}")
    print(f"Function: {call.function.name}")
    print(f"Arguments: {call.function.arguments}")
