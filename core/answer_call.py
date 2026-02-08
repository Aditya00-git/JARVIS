# import pyautogui
# import time

# def whatsapp_answer_call():
#     pyautogui.FAILSAFE = False

#     for _ in range(30):  # try for 15 sec
#         loc = pyautogui.locateOnScreen(
#             "accept_call.png",
#             confidence=0.8
#         )

#         if loc:
#             pyautogui.click(pyautogui.center(loc))
#             return True

#         time.sleep(0.5)

#     return False
