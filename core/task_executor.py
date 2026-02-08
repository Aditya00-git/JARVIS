from core import action_engine as ae
import time
import pyautogui


def execute_plan(plan):
    for step in plan:
        action = step.get("action")
        args = step.get("args", [])

        try:
            # ---------------- BASIC ACTIONS ----------------

            if action == "wait":
                ae.wait(*args)

            elif action == "press":
                ae.press(*args)

            elif action == "hotkey":
                ae.hotkey(*args)

            elif action == "click":
                ae.click(*args)

            elif action == "focus":
                ae.focus(*args)

            # ---------------- TYPING ----------------
            elif action == "type":
                # type wherever cursor is
                ae.type_text(*args)

            # ---------------- SEARCH (BROWSER ONLY) ----------------
            elif action == "search":
                query = args[0]

                # focus browser address bar
                ae.hotkey("ctrl", "l")
                ae.wait(0.2)

                ae.type_text(query)
                ae.wait(0.1)
                ae.press("enter")

            # ---------------- CLICK CENTER (OPTIONAL) ----------------
            elif action == "click_center":
                w, h = pyautogui.size()
                pyautogui.click(w // 2, h // 2)

        except Exception as e:
            # silent fail to keep Jarvis alive
            continue
