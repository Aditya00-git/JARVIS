import json
import os

MEMORY_FILE = "memory.json"


def _load():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def _save(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def remember(category, key, value):
    data = _load()
    if category not in data:
        data[category] = {}
    data[category][key] = value
    _save(data)


def recall(category, key=None):
    data = _load()
    if category not in data:
        return None
    if key:
        return data[category].get(key)
    return data[category]


def forget(category, key=None):
    data = _load()
    if category not in data:
        return
    if key:
        data[category].pop(key, None)
    else:
        data.pop(category)
    _save(data)
