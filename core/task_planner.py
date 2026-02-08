import os
from openai import OpenAI
import json




SYSTEM_PROMPT = """
You are a desktop automation AI.

Convert the user command into a list of actions.

ONLY output valid JSON.
DO NOT explain anything.
DO NOT use markdown.
DO NOT add text outside JSON.

Allowed actions:
- focus
- hotkey
- type
- press
- wait

JSON FORMAT EXAMPLE:
[
  {"action": "focus", "args": ["Chrome"]},
  {"action": "hotkey", "args": ["ctrl", "l"]},
  {"action": "type", "args": ["youtube ai news"]},
  {"action": "press", "args": ["enter"]}
]
"""

def plan_task(command):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": command}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)
