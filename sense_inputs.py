import pygame

pygame.init()
screen = pygame.display.set_mode((250, 120))
pygame.display.set_caption("DualSense Dinleyici")
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("DualSense bulunamadı!")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()

print("=" * 45)
print(f"Bağlandı: {controller.get_name()}")
print(
    f"Toplam Buton: {controller.get_numbuttons()} | Toplam Eksen: {controller.get_numaxes()} | Hat (D-Pad): {controller.get_numhats()}"
)
print("Koldaki tuşlara basıp analoğu oynatabilirsin...")
print("=" * 45)

# DualSense standart buton dizilimi (Pygame/SDL2 indeksleri)
BUTTON_NAMES = {
    0: "(X)",
    1: "(○)",
    2: "(□)",
    3: "(△)",
    4: "(Share)",
    5: "(PS btn)",
    6: "(Options)",
    7: "(L3)",
    8: "(R3)",
    9: "(L1)",
    10: "(R1)",
    11: "(↑)",
    12: "(↓)",
    13: "(<-)",
    14: "(->)",
}

# Eksen tanımlamaları
AXIS_NAMES = {
    0: "Sol Analog (Yatay: Sol - / Sağ +)",
    1: "Sol Analog (Dikey: Yukarı - / Aşağı +)",
    2: "Sağ Analog (Yatay: Sol - / Sağ +)",
    3: "Sağ Analog (Dikey: Yukarı - / Aşağı +)",
    4: "L2 Tetiği (Analog)",
    5: "R2 Tetiği (Analog)",
}

try:
    while True:
        # Event kuyruğundaki tüm olayları yakala
        for event in pygame.event.get():

            # Pencere kapatma butonu
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

            # 1. BUTON BASILDI
            elif event.type == pygame.JOYBUTTONDOWN:
                btn_id = event.button
                name = BUTTON_NAMES.get(btn_id, f"Bilinmeyen Buton {btn_id}")
                print(f"[BUTON BASILDI]  ID: {btn_id:<2} : {name}")

            # 2. BUTON BIRAKILDI
            elif event.type == pygame.JOYBUTTONUP:
                btn_id = event.button
                name = BUTTON_NAMES.get(btn_id, f"Bilinmeyen Buton {btn_id}")
                print(f"[BUTON BIRAKILDI] ID: {btn_id:<2} : {name}")

            # 3. D-PAD (Yön Butonları)
            elif event.type == pygame.JOYHATMOTION:
                x, y = event.value
                yonler = []
                if y == 1:
                    yonler.append("Yukarı")
                elif y == -1:
                    yonler.append("Aşağı")
                if x == 1:
                    yonler.append("Sağ")
                elif x == -1:
                    yonler.append("Sol")

                durum = " + ".join(yonler) if yonler else "Bırakıldı / Boşta"
                print(f"[D-PAD]          Değer: {event.value} -> {durum}")

            # 4. ANALOG VE TETİKLER (Eksen Hareketi)
            elif event.type == pygame.JOYAXISMOTION:
                axis_id = event.axis
                val = event.value

                # L2/R2 tetikleri boştayken -1.0 üretir; basıldığında tetikle
                if axis_id in (4, 5):
                    if val > -0.8:  # Hafif basılma eşiği
                        print(
                            f"[TETİK HAREKETİ] {AXIS_NAMES.get(axis_id, axis_id)} Değer: {val:.2f}"
                        )

                # Sol/Sağ Analog için ölü bölge (deadzone) filtresi
                elif abs(val) > 0.3:
                    print(
                        f"[ANALOG HAREKET] {AXIS_NAMES.get(axis_id, axis_id)} Değer: {val:.2f}"
                    )

except KeyboardInterrupt:
    pygame.quit()
    print("\nProgram kapatıldı.")
