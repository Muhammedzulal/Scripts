import pygame
import pydirectinput
import time

pydirectinput.PAUSE = 0
pydirectinput.FAILSAFE = False

# ============================================================
#  TANIMLAR - SADECE BURAYI DEĞİŞTİR
# ============================================================

# D-Pad (11, 12, 13, 14) tuşlarını slot sistemi için aşağıda özel olarak yöneteceğiz.
BUTTON_TO_KEY = {
    0: "space",  # (X)      -> Zıpla
    1: "e",  # (○)      -> Envanter
    2: "ctrl",  # (□)      -> Yeniden doldur / kullan
    3: "q",  # (△)      -> Eşya at
    4: "tab",  # (Share)
    5: "esc",  # (PS btn) -> Menü
    6: "escape",  # (Options)-> Duraklat
    7: "f3",  # (L3)     -> Çömel/koş toggle
    8: "f",  # (R3)
    9: "shift",  # (L1)     -> Sprint
    10: "f5",  # (R1)     -> kamera
}

# Konsol çıktıları için tuş isimleri
BUTTON_NAMES = {
    0: "(X)",
    1: "(O)",
    2: "(□)",
    3: "(△)",
    4: "(Share)",
    5: "(PS)",
    6: "(Options)",
    7: "(L3)",
    8: "(R3)",
    9: "(L1)",
    10: "(R1)",
    11: "(D-Pad Yukarı)",
    12: "(D-Pad Aşağı)",
    13: "(D-Pad Sol)",
    14: "(D-Pad Sağ)",
}

LEFT_STICK_KEYS = {
    "up": "w",
    "down": "s",
    "left": "a",
    "right": "d",
}

# L2 / R2 tetikleri -> FARE TIKLAMASI (mouse button: "left" / "right" / "middle")
TRIGGER_TO_MOUSE = {
    4: "right",  # L2  -> Sol tık (kırma)
    5: "left",  # R2  -> Sağ tık (yerleştirme/nişan)
}

TRIGGER_NAMES = {4: "(L2)", 5: "(R2)"}

STICK_DEADZONE = 0.35
TRIGGER_THRESHOLD = 0.5

MOUSE_DEADZONE = 0.15
MOUSE_SENSITIVITY = 25
INVERT_Y = False

# ============================================================
#  KOD KISMI
# ============================================================

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Kontrolcü bulunamadı!")
    exit()

joy = pygame.joystick.Joystick(0)
joy.init()
print(f"Bağlandı: {joy.get_name()}")

active_keys = set()
active_mouse_buttons = set()
stick_state = {"left": False, "down": False, "right": False, "up": False}
trigger_state = {}

# Slot takibi için değişken (Min: 1, Max: 9)
current_slot = 1


def key_down(key, log_msg=None):
    if key and key not in active_keys:
        pydirectinput.keyDown(key)
        active_keys.add(key)
        if log_msg:
            print(log_msg)


def key_up(key):
    if key and key in active_keys:
        pydirectinput.keyUp(key)
        active_keys.discard(key)


def mouse_down(button, log_msg=None):
    if button and button not in active_mouse_buttons:
        pydirectinput.mouseDown(button=button)
        active_mouse_buttons.add(button)
        if log_msg:
            print(log_msg)


def mouse_up(button):
    if button and button in active_mouse_buttons:
        pydirectinput.mouseUp(button=button)
        active_mouse_buttons.discard(button)


def handle_left_stick(x, y):
    if x < -STICK_DEADZONE:
        if not stick_state["left"]:
            key_down(
                LEFT_STICK_KEYS["left"], f"(L-Stick Sol) -> ({LEFT_STICK_KEYS['left']})"
            )
            stick_state["left"] = True
    elif stick_state["left"]:
        key_up(LEFT_STICK_KEYS["left"])
        stick_state["left"] = False

    if x > STICK_DEADZONE:
        if not stick_state["right"]:
            key_down(
                LEFT_STICK_KEYS["right"],
                f"(L-Stick Sağ) -> ({LEFT_STICK_KEYS['right']})",
            )
            stick_state["right"] = True
    elif stick_state["right"]:
        key_up(LEFT_STICK_KEYS["right"])
        stick_state["right"] = False

    if y < -STICK_DEADZONE:
        if not stick_state["up"]:
            key_down(
                LEFT_STICK_KEYS["up"], f"(L-Stick Yukarı) -> ({LEFT_STICK_KEYS['up']})"
            )
            stick_state["up"] = True
    elif stick_state["up"]:
        key_up(LEFT_STICK_KEYS["up"])
        stick_state["up"] = False

    if y > STICK_DEADZONE:
        if not stick_state["down"]:
            key_down(
                LEFT_STICK_KEYS["down"],
                f"(L-Stick Aşağı) -> ({LEFT_STICK_KEYS['down']})",
            )
            stick_state["down"] = True
    elif stick_state["down"]:
        key_up(LEFT_STICK_KEYS["down"])
        stick_state["down"] = False


def handle_mouse_stick(x, y):
    dx = x if abs(x) > MOUSE_DEADZONE else 0
    dy = y if abs(y) > MOUSE_DEADZONE else 0
    if dx == 0 and dy == 0:
        return
    move_x = int(dx * MOUSE_SENSITIVITY)
    move_y = int(dy * MOUSE_SENSITIVITY)
    if INVERT_Y:
        move_y = -move_y
    if move_x != 0 or move_y != 0:
        pydirectinput.moveRel(move_x, move_y, relative=True)


print("Dönüştürücü çalışıyor... Çıkmak için Ctrl+C")

try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                btn = event.button
                btn_name = BUTTON_NAMES.get(btn, f"(Buton {btn})")

                # Slot Geçiş Sistemi
                if btn == 14:  # D-Pad Sağ (Sonraki Slot)
                    if current_slot < 9:
                        current_slot += 1
                    print(f"{btn_name} -> (Slot {current_slot}) [Tuş: {current_slot}]")
                    pydirectinput.press(str(current_slot))

                elif btn == 13:  # D-Pad Sol (Önceki Slot)
                    if current_slot > 1:
                        current_slot -= 1
                    print(f"{btn_name} -> (Slot {current_slot}) [Tuş: {current_slot}]")
                    pydirectinput.press(str(current_slot))

                elif btn in (11, 12):  # D-Pad Yukarı ve Aşağı boşa çıkarıldı
                    print(f"{btn_name} -> (Atanmadı)")

                else:
                    key = BUTTON_TO_KEY.get(btn)
                    if key:
                        key_down(key, f"{btn_name} -> ({key})")
                    else:
                        print(f"{btn_name} -> (Tanımsız)")

            elif event.type == pygame.JOYBUTTONUP:
                key = BUTTON_TO_KEY.get(event.button)
                if key:
                    key_up(key)
            elif event.type == pygame.QUIT:
                running = False

        lx, ly = joy.get_axis(0), joy.get_axis(1)
        handle_left_stick(lx, ly)

        if joy.get_numaxes() > 3:
            rx, ry = joy.get_axis(2), joy.get_axis(3)
            handle_mouse_stick(rx, ry)

        # Tetikler -> mouse tıklaması
        for axis_id, button in TRIGGER_TO_MOUSE.items():
            if axis_id < joy.get_numaxes():
                val = joy.get_axis(axis_id)
                pressed = val > TRIGGER_THRESHOLD
                was_pressed = trigger_state.get(axis_id, False)

                trig_name = TRIGGER_NAMES.get(axis_id, f"(Tetik {axis_id})")

                if pressed and not was_pressed:
                    mouse_down(button, f"{trig_name} -> (Fare {button} tık)")
                elif not pressed and was_pressed:
                    mouse_up(button)
                trigger_state[axis_id] = pressed

        time.sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    for k in list(active_keys):
        pydirectinput.keyUp(k)
    for b in list(active_mouse_buttons):
        pydirectinput.mouseUp(button=b)
    pygame.quit()
    print("Kapatıldı.")
