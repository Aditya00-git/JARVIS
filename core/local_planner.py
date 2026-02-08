def plan_local(command: str):
    command = command.lower().strip()
    steps = []

    # normalize speech quirks
    command = command.replace("&", "and")
        # -------- SEARCH ONLY (ASSUME BROWSER OPEN) --------
    if command.startswith("search"):
        query = command.replace("search", "").replace("for", "").strip()

        return [
            {"action": "hotkey", "args": ["ctrl", "l"]},
            {"action": "type", "args": [query]},
            {"action": "press", "args": ["enter"]}
        ]

        # -------- GENERIC TYPE COMMAND --------
    if command.startswith("type ") or command.startswith("write "):
        text = (
            command.replace("type", "")
            .replace("write", "")
            .strip()
        )

        return [
            {"action": "type", "args": [text]},
            {"action": "press", "args": ["enter"]}
        ]

    # -------- OPEN + SEARCH --------
    if command.startswith("open") and "search" in command:
        # works for:
        # open chrome search youtube for ai news
        # open chrome and search youtube for ai news

        parts = command.split("search", 1)
        app_part = parts[0]
        query_part = parts[1]

        app = (
            app_part.replace("open", "")
            .replace("and", "")
            .strip()
        )

        query = query_part.replace("for", "").strip()

        steps.append({"action": "focus", "args": [app]})
        steps.append({"action": "hotkey", "args": ["ctrl", "l"]})
        steps.append({"action": "type", "args": [query]})
        steps.append({"action": "press", "args": ["enter"]})
        return steps

    # -------- OPEN + TYPE --------
    if command.startswith("open") and "type" in command:
        # open whatsapp type hello
        parts = command.split("type", 1)
        app_part = parts[0]
        text = parts[1].strip()

        app = (
            app_part.replace("open", "")
            .replace("and", "")
            .strip()
        )

        steps.append({"action": "focus", "args": [app]})
        steps.append({"action": "wait", "args": [1]})

        # 🔑 click center of screen to focus input (works for chat apps)
        steps.append({"action": "click", "args": ["center"]})

        steps.append({"action": "type", "args": [text]})
        steps.append({"action": "press", "args": ["enter"]})

        return steps

    return None
