import subprocess

def ask_local_ai(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "tinyllama"],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=12
        )
        return result.stdout.strip()
    except Exception:
        return ""
