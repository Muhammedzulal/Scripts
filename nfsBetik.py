import os

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import pydirectinput
import time

pydirectinput.PAUSE = 0.0
pydirectinput.FAILSAFE = False

pygame.init()
screen = pygame.display.set_mode((200, 100))
pygame.display.set_caption("NFS DualSense")
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("DualSense bulunamadı!")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()
print(f"Bağlandı: {controller.get_name()}")

DEADZONE = 0.35

# ==========================================
# 🎮 KONTROL ŞEMASI (Güncel ID'lere Göre)
# ==========================================
NFS_KEYBINDINGS = {
    # -- Yön / Direksiyon (Sol Analog - Axis 0 & 1) --
    "steer_left": "left",
    "steer_right": "right",
    # -- Temel Sürüş --
    "accelerate": "up",  # X Butonu (ID: 0)
    "brake_reverse": "down",  # Kare Butonu (ID: 2)
    "speedbreaker": "g",  # Üçgen Butonu (ID: 3)
    "look_back": "l",  # Yuvarlak Butonu (ID: 1)
    # -- Üst Tetikler ve Tamponlar --
    "nitrous": "alt",  # L1 Butonu (ID: 9)
    "ebrake": "space",  # R1 Butonu (ID: 10)
    "shift_down": "ctrl",  # L2 Tetiği (Axis 4)
    "shift_up": "shift",  # R2 Tetiği (Axis 5)
    # -- D-Pad (Yön Tuşları) --
    "enter_shop": "enter",  # D-Pad Yukarı (ID: 11)
    "blacklist": "b",  # D-Pad Aşağı (ID: 12)
    "world_map": "m",  # D-Pad Sol (ID: 13)
    "sms_system": "tab",  # D-Pad Sağ (ID: 14)
    # -- Sistem --
    "reset_car": "r",  # Share Butonu (ID: 4)
    "pause_game": "esc",  # Options Butonu (ID: 6)
}

keys_pressed = {key: False for key in NFS_KEYBINDINGS.values()}


def update_key(action_name, should_press):
    """
    Hedef aksiyonun klavye tuşunu alır ve sadece durum değiştiğinde bas/bırak yapar.
    """
    key = NFS_KEYBINDINGS[action_name]

    if should_press and not keys_pressed[key]:
        pydirectinput.keyDown(key)
        keys_pressed[key] = True
        print(f"[BASILDI] -> {action_name} ({key})")
    elif not should_press and keys_pressed[key]:
        pydirectinput.keyUp(key)
        keys_pressed[key] = False
        print(f"[BIRAKILDI] -> {action_name} ({key})")


def process_nfs_controls():
    """
    Tüm DualSense girdilerini okur ve yeni ID eşleştirmelerine göre çevirir.
    """
    # Güvenlik için toplam buton sayısını al (Sınır aşımını engeller)
    num_btns = controller.get_numbuttons()

    # 1. Analog Eksenleri Okuma
    stick_x = controller.get_axis(0)

    # 2. D-Pad (Hat) Okuma - Yedek Algılayıcı
    dpad_x, dpad_y = (0, 0)
    if controller.get_numhats() > 0:
        dpad_x, dpad_y = controller.get_hat(0)

    # ==========================================
    # ⚙️ GİRDİLERİ KLAVYEYE EŞLEME
    # ==========================================

    # Direksiyon (Sol Analog)
    update_key("steer_left", stick_x < -DEADZONE)
    update_key("steer_right", stick_x > DEADZONE)

    # Temel Sürüş
    update_key("accelerate", controller.get_button(0) if num_btns > 0 else False)
    update_key("brake_reverse", controller.get_button(2) if num_btns > 2 else False)
    update_key("speedbreaker", controller.get_button(3) if num_btns > 3 else False)
    update_key("look_back", controller.get_button(1) if num_btns > 1 else False)

    # Tamponlar (L1/R1 - Yeni ID: 9 ve 10)
    update_key("nitrous", controller.get_button(9) if num_btns > 9 else False)
    update_key("ebrake", controller.get_button(10) if num_btns > 10 else False)

    # Tetikler (L2/R2 - Axis 4 ve 5)
    l2_axis = controller.get_axis(4) if controller.get_numaxes() > 4 else -1.0
    r2_axis = controller.get_axis(5) if controller.get_numaxes() > 5 else -1.0

    # Tetik boştayken -1.0'dır. -0.8'i geçerse basıldı say.
    update_key("shift_down", l2_axis > -0.8)
    update_key("shift_up", r2_axis > -0.8)

    # Menü ve D-Pad (İster Hat olarak gelsin, ister 11, 12, 13, 14 numaralı butonlar olarak)
    up_pressed = (dpad_y == 1) or (num_btns > 11 and controller.get_button(11))
    down_pressed = (dpad_y == -1) or (num_btns > 12 and controller.get_button(12))
    left_pressed = (dpad_x == -1) or (num_btns > 13 and controller.get_button(13))
    right_pressed = (dpad_x == 1) or (num_btns > 14 and controller.get_button(14))

    update_key("enter_shop", up_pressed)
    update_key("blacklist", down_pressed)
    update_key("world_map", left_pressed)
    update_key("sms_system", right_pressed)

    # Sistem (Share - ID: 4, Options - ID: 6)
    update_key("reset_car", controller.get_button(4) if num_btns > 4 else False)
    update_key("pause_game", controller.get_button(6) if num_btns > 6 else False)


try:
    print("NFS Hazır! DualSense okuması başladı...")
    while True:
        # Event kuyruğunu tüket
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        process_nfs_controls()
        time.sleep(0.005)

except KeyboardInterrupt:
    for key, is_down in keys_pressed.items():
        if is_down:
            pydirectinput.keyUp(key)
    pygame.quit()
    print("\nTuşlar serbest bırakıldı, çıkış yapıldı.")
