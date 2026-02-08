from core.listener import listen
from core.app_launcher import open_app_by_name
from core.spotify_control import play_pause, next_song
from core.speaker import jarvis_say
from core.sound import play_sound
from core.local_planner import plan_local
from core.task_executor import execute_plan
from core.call_actions import whatsapp_voice_call
from core.call_actions import whatsapp_video_call
from core.memory import remember, recall, forget
from core.chain_parser import split_chain
from core.ai_normalizer import normalize_command

import time

last_command_time = 0
COMMAND_COOLDOWN = 1.2  # seconds
command_executed = False

def run_jarvis(ui):
    jarvis_say("Jarvis is online")
    play_sound("online.wav")

    while True:
        # 💤 SLEEP MODE — wait ONLY for wake word
        ui.state_signal.emit("listening")
        wake_phrase = listen(timeout=6, phrase_time_limit=3)

        if not wake_phrase or "hey jarvis" not in wake_phrase:
            continue

        # 👀 WAKE UP
        ui.state_signal.emit("speaking")
        jarvis_say("Yes?")
        command_executed = False

        ui.state_signal.emit("idle")
        time.sleep(0.3)

        # 🎯 LISTEN FOR ONE COMMAND
                # 🎯 LISTEN FOR ONE COMMAND
        command = listen(timeout=6, phrase_time_limit=6)

        if command is None:
            continue

        command = command.lower().strip()

        # 🤖 AI NORMALIZATION (ONCE, BEFORE CHAINING)
        if not command.startswith(("open", "type", "call", "search")):
            ai_cmd = normalize_command(command)
            if ai_cmd:
                command = ai_cmd

        # ⏱️ COOLDOWN (ANTI DOUBLE EXECUTION)
        now = time.time()
        global last_command_time
        if now - last_command_time < COMMAND_COOLDOWN:
            continue
        last_command_time = now

        # 🔗 SPLIT INTO CHAIN
        commands = split_chain(command)

        for cmd in commands:
            cmd = cmd.strip()

            # EXIT
            if "bye bye" in cmd or "shutdown jarvis" in cmd:
                jarvis_say("Jarvis is going offline")
                play_sound("offline.wav")
                return

            # TYPE
            if cmd.startswith("type") or cmd.startswith("write"):
                text = cmd.replace("type", "").replace("write", "").strip()
                jarvis_say("Typing")
                execute_plan([
                    {"action": "type", "args": [text]},
                    {"action": "press", "args": ["enter"]}
                ])
                time.sleep(0.4)
                continue

            # CALL
            if "call" in cmd:
                jarvis_say("Starting call")
                whatsapp_voice_call()
                time.sleep(0.5)
                continue

            # OPEN APP
            # OPEN COMMAND
            if cmd.startswith("open"):
                target = cmd.replace("open", "").strip()

                # 🌐 WEB TARGETS
                web_targets = ["youtube", "google", "gmail", "facebook", "instagram"]

                if target in web_targets:
                    jarvis_say(f"Opening {target}")
                    execute_plan([
                        {"action": "open_browser", "args": []},
                        {"action": "search", "args": [target]}
                    ])
                    time.sleep(1)
                    continue

                # 🖥️ LOCAL APP
                jarvis_say(f"Opening {target}")
                open_app_by_name(target)
                command_executed = True
                time.sleep(1)
                continue


            # MEDIA
            if "play" in cmd or "pause" in cmd:
                jarvis_say("Okay")
                play_pause()
                time.sleep(0.3)
                continue

            if "next" in cmd:
                jarvis_say("Skipping")
                next_song()
                time.sleep(0.5)
                continue

            # MEMORY
            if "remember my name is" in cmd:
                name = cmd.replace("remember my name is", "").strip()
                remember("profile", "name", name)
                jarvis_say(f"I will remember your name is {name}")
                continue

            if "what is my name" in cmd:
                name = recall("profile", "name")
                jarvis_say(f"Your name is {name}" if name else "I don't know your name yet")
                continue

            # 🧠 LOCAL PLANNER (SEARCH ETC.)
            plan = plan_local(cmd)

            if not plan:
                jarvis_say("I don't know how to do that")
                break

            jarvis_say("Working on it")
            execute_plan(plan)
            jarvis_say("Done")
            time.sleep(0.5)


