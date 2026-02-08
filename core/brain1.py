from core.listener import listen
from core.app_launcher import open_app_by_name
from core.spotify_control import play_pause, next_song
from core.speaker import jarvis_say
from core.sound import play_sound
from core.task_executor import execute_plan
from core.call_actions import whatsapp_voice_call
import time
import random
import os
from core.system_monitor import start_system_monitor
from core.screen_awareness import get_active_app, read_selected_text, copy_selected_text
from core.screen_awareness import *
from core.hotword import HotwordDetector
from core.chain_parser import split_chain
from core.ai_normalizer import normalize_command
from core.system_control import *
# from core.answer_call import whatsapp_answer_call
from core.call_actions import whatsapp_cut_call
from core.call_actions import whatsapp_answer_call
from core.call_actions import whatsapp_end_call
from core.call_actions import whatsapp_mute_call
from core.call_actions import start_call_watcher
start_call_watcher()
from core.audio_level1 import audio_level
from core.system_scan import system_scan
import keyboard
IGNORE_AFTER_COMMAND = 2.0 
hotword = HotwordDetector()
hotword.start() # seconds
last_wake = None
def play_random_wake():
    global last_wake
    folder = os.path.join(os.path.dirname(__file__), "..", "sounds", "wake")
    folder = os.path.abspath(folder)
    files = [f for f in os.listdir(folder) if f.endswith(".wav")]
    choices = [f for f in files if f != last_wake]
    sound = random.choice(choices or files)
    last_wake = sound
    play_sound(os.path.join(folder, sound))
def run_jarvis(ui):
    start_system_monitor()
    last_action_time = 0
    play_sound("real.wav")
    play_sound("home.wav")
    while True:
        time.sleep(0.01)
        WAKE_WORDS = [
            "hey jarvis",
            "jarvis"
        ]
        def is_wake_word(text):
            return any(w in text for w in WAKE_WORDS)
        INTERRUPTS = ["stop", "cancel", "wait", "enough"]
        def is_interrupt(command):
            return any(word in command for word in INTERRUPTS)
        def keyboard_wake():
            return keyboard.is_pressed("ctrl+space")
        ui.state_signal.emit("listening")
        audio_level.running = False
        hotword.wait()
        audio_level.running = True   
        wake_phrase = "jarvis"
        if keyboard_wake():
            wake_phrase = "jarvis"
        if not wake_phrase or not is_wake_word(wake_phrase):
            continue
        ui.state_signal.emit("speaking")
        play_random_wake()
        if time.time() - last_action_time < IGNORE_AFTER_COMMAND:
            continue
        ui.state_signal.emit("idle")
        time.sleep(0.25)  
        hotword.stop()  
        audio_level.running = False  
        command = listen(timeout=5, phrase_time_limit=6)
        audio_level.running = True 
        if command is None:
            continue
        command = command.lower().strip()
        if is_interrupt(command):
            jarvis_say("Okay")
            play_sound("doingtask.wav")
            ui.state_signal.emit("idle")
            continue
        if ("message" in command or "send" in command) and "whatsapp" in command:
            text = command
            for word in ["please", "message", "send", "on whatsapp", "whatsapp", "to"]:
                text = text.replace(word, "")
            text = text.strip()
            play_sound("opening.wav")
            open_app_by_name("whatsapp")
            time.sleep(2)
            if text:
                jarvis_say("Typing message")
                execute_plan([
                    {"action": "type", "args": [text]},
                    {"action": "press", "args": ["enter"]}
                ])
                play_sound("taskcompleted.wav")
            continue
        if not command.startswith(("open", "type", "call", "search","message","send")):
            ai_cmd = normalize_command(command)
            if ai_cmd and any(ai_cmd.startswith(k) for k in ("open", "type", "call", "search")):
                command = ai_cmd
        commands = split_chain(command)
        web_targets = ["youtube", "google", "gmail", "facebook", "instagram"]
        for cmd in commands:
            cmd = cmd.strip()
            if "scan system" in cmd or "system status" in cmd or cmd == "scan":
                ui.state_signal.emit("thinking")
                ui.scan_show_signal.emit("SYSTEM INITIALIZING...")
                play_sound("system.wav")
                stats = system_scan()
                def finish_scan():
                    ui.scan_hide_signal.emit()
                    report = (
                        f"CPU {stats['cpu']} percent, "
                        f"Memory {stats['ram']} percent, "
                    )
                    if stats["battery"] is not None:
                        report += f"Battery {stats['battery']} percent, "
                    report += f"Network {stats['network']}"
                    jarvis_say(report)
                    ui.state_signal.emit("success")
                    time.sleep(1.5)
                finish_scan()
                continue
            if "bye bye" in cmd or "shutdown jarvis" in cmd or "go  " in cmd:
                play_sound("test2.wav")
                hotword.stop()
                ui.close_signal.emit()   
                return 
            if cmd.startswith("open"):
                target = cmd.replace("open", "").strip()
                if target in web_targets:
                    play_sound("opening.wav")
                    open_app_by_name("chrome")
                    time.sleep(0.8)
                    execute_plan([
                        {"action": "search", "args": [target]}
                    ])
                    time.sleep(0.6)    
                    continue
                play_sound("opening.wav")
                open_app_by_name(target)
                ui.notify_msg(f"{target} opened")
                ui.state_signal.emit("success")
                time.sleep(0.6)
                continue
            if cmd.startswith("type"):
                text = cmd.replace("type", "").strip()
                play_sound("doingtask.wav")
                play_sound("typing.wav")
                execute_plan([
                    {"action": "type", "args": [text]},
                    {"action": "press", "args": ["enter"]}
                ])
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Message sent")
                time.sleep(0.3)
                continue
            if "make phone call" in cmd:
                play_sound("doingtask.wav")
                whatsapp_voice_call()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Call done")
                time.sleep(0.6)
                continue
            if "answer call" in cmd:
                play_sound("answered.wav")
                whatsapp_answer_call()
                continue
            if "cut call" in cmd or "reject call" in cmd or "decline call" in cmd:
                play_sound("declined.wav")
                whatsapp_cut_call()
                continue
            if "mute call" in cmd:
                jarvis_say("Call muted")
                whatsapp_mute_call()
                continue
            if "end call" in cmd or "hang up" in cmd:
                jarvis_say("Call ending Sir")
                whatsapp_end_call()
                continue
            if "play" in cmd or "stop" in cmd:      
                play_sound("doingtask.wav")
                play_pause()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Music played")
                time.sleep(0.3)
                continue
            if "next" in cmd:           
                play_sound("doingtask.wav")
                next_song()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                time.sleep(0.3)
                continue
            if "previous" in cmd or "back" in cmd:
                play_sound("doingtask.wav")
                keyboard.send("media previous track")
                play_sound("taskcompleted.wav")
                time.sleep(0.3)
                continue
            if "volume up" in cmd:
                play_sound("doingtask.wav")
                keyboard.send("volume up")
                continue
            if "volume down" in cmd:
                play_sound("doingtask.wav")
                keyboard.send("volume down")
                play_sound("taskcompleted.wav")
                continue
            if "mute" in cmd:
                play_sound("doingtask.wav")
                keyboard.send("volume mute")
                play_sound("taskcompleted.wav")
                continue
            if "volume up" in cmd:
                play_sound("doingtask.wav")
                volume_up()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Volume increased")
                continue
            if "volume down" in cmd:
                play_sound("doingtask.wav")
                volume_down()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("volume decreased")
                continue
            if "mute" in cmd:
                play_sound("doingtask.wav")
                mute()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Muted")
                continue
            if "brightness up" in cmd:
                play_sound("doingtask.wav")
                brightness_up()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Brightness increased")
                continue
            if "brightness down" in cmd:
                play_sound("doingtask.wav")
                brightness_down()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Brightness decreased")
                continue
            if "lock pc" in cmd or "lock computer" in cmd:
                play_sound("locking.wav")
                lock_pc()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Computer locked")
                continue
            if "sleep pc" in cmd:
                play_sound("sleep.wav")
                sleep_pc()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                ui.notify_msg("Computer sleeps")
                continue
            if "shutdown pc" in cmd:
                jarvis_say("Shutting down")
                shutdown_pc()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                continue
            if "restart pc" in cmd:
                play_sound("restarting.wav")
                restart_pc()
                ui.state_signal.emit("success")
                play_sound("taskcompleted.wav")
                continue
            if "what app" in cmd or "which app" in cmd:
                app = get_active_app()
                jarvis_say(f"You are using {app}")
                ui.state_signal.emit("success")
                continue
            if "read selected" in cmd or "read this" in cmd:
                text = read_selected_text()
                if text:
                    jarvis_say(text[:200])
                    ui.state_signal.emit("success")
                else:
                    jarvis_say("Nothing selected")
                    ui.state_signal.emit("error")
                continue
            if "copy" in cmd:
                text = copy_selected_text()
                if text:
                    jarvis_say("Copied")
                    ui.state_signal.emit("success")
                else:
                    jarvis_say("Nothing selected")
                    ui.state_signal.emit("error")
                continue
            if "what did i copy" in cmd or "read clipboard" in cmd:
                text = get_clipboard()
                if text:
                    jarvis_say(text[:200])
                    ui.state_signal.emit("success")
                else:
                    jarvis_say("Clipboard is empty")
                    ui.state_signal.emit("error")
                continue
            if "paste" in cmd or "paste here" in cmd:
                paste_clipboard()
                jarvis_say("Pasted")
                ui.state_signal.emit("success")
                continue
            if "minimize window" in cmd:
                minimize_window()
                jarvis_say("Minimized")
                ui.state_signal.emit("success")
                continue
            if "Full Screen" in cmd:
                maximize_window()
                jarvis_say("Maximized")
                ui.state_signal.emit("success")
                continue
            if "close window" in cmd:
                close_window()
                jarvis_say("Window Closed")
                ui.state_signal.emit("success")
                continue
            if "switch window" in cmd:
                switch_window()
                jarvis_say("Window Switched")
                ui.state_signal.emit("success")
                continue
            if "take screenshot" in cmd:
                file = take_screenshot()
                jarvis_say("Screenshot saved")
                ui.state_signal.emit("success")
                ui.notify_msg(file)
                continue
            if "scroll down" in cmd:
                scroll_down()
                continue
            if "scroll up" in cmd:
                scroll_up()
                continue
            if "bye bye" in cmd or "shutdown jarvis" in cmd:
                jarvis_say("Jarvis is going offline")
                play_sound("offline.wav")
                return
            jarvis_say("Hmmmmm")
            ui.state_signal.emit("error")
            play_sound("error.wav")
            break
            hotword.start()