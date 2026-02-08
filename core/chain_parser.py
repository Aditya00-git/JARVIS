def split_chain(command: str):
    command = command.lower()
    if " then " in command:
        return [c.strip() for c in command.split(" then ")]
    return [command]
