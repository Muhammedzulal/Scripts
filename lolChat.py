import time
import pydirectinput

print("Çalışıyor...")

while True:
    pydirectinput.press("enter")
    time.sleep(0.2)

    # Türkçe Q klavyede /
    pydirectinput.keyDown("shift")
    pydirectinput.press("7")
    pydirectinput.keyUp("shift")

    time.sleep(0.05)

    for char in "resume":
        pydirectinput.press(char)
        time.sleep(0.02)

    pydirectinput.press("enter")
    time.sleep(7)
