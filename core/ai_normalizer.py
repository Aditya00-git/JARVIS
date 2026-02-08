from core.local_ai import ask_local_ai

SYSTEM_PROMPT = """
You convert user speech into assistant commands.

Rules:
- lowercase only
- no punctuation
- no explanations
- only use: open, search, type, call, then

Examples:
User: can you open youtube and search ai news
Output: open chrome then search youtube for ai news

User: text hello on whatsapp
Output: open whatsapp then type hello

User: please text hello on whatsapp
Output: open whatsapp then type hello

User: send hello to john on whatsapp
Output: open whatsapp then type hello
"""

def normalize_command(text: str) -> str:
    prompt = SYSTEM_PROMPT + "\nUser: " + text + "\nOutput:"
    result = ask_local_ai(prompt)
    return result.lower().strip()
