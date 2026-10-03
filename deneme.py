import pygame
import pydirectinput

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Kontrolcü bulunamadı!")
    exit()

joy = pygame.joystick.Joystick(0)
joy.init()
print()
print(f"Bağlandı: {joy.get_name()}")

# Sadece dinlemek istediğimiz şekil tuşları
BUTTONS = {0: "(X)", 1: "(O)", 2: "(#)", 3: "(^)"}


try:
    while True:
        for event in pygame.event.get():
            # Butona ilk basıldığı anı yakalar
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button in BUTTONS:
                    print(f"Basıldı: {BUTTONS[event.button]}")
                    # pydirectinput.press("1")
            elif event.type == pygame.JOYBUTTONUP:
                if event.button in BUTTONS:
                    print(f"Çekildi: {BUTTONS[event.button]}")
                    # pydirectinput.press("2")

except KeyboardInterrupt:
    pass
finally:
    pygame.quit()
    print("Kapatıldı.")
