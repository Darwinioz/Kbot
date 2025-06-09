import pyautogui
import time
import os

CONFIG_PATH = "config.txt"
IMAGE_PATH = os.path.join("images", "dofus2")

pyautogui.USE_IMAGE_NOT_FOUND_EXCEPTION = False

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            lines = f.read().splitlines()
            if len(lines) < 7 or lines[6].lower() == "off":
                print("⛔ Bot désactivé ou config vide.")
                return None
            version = lines[0].strip()
            mode = lines[1].strip()
            coords = lines[2].strip()
            delay = float(lines[3].strip())
            spell_key = lines[4].strip()
            alt_spell_key = lines[5].strip()
            x, y = map(int, coords.split(","))
            return {
                "version": version,
                "mode": mode,
                "coords": (x, y),
                "delay": delay,
                "spell_key": spell_key,
                "alt_spell_key": alt_spell_key
            }
    except Exception as e:
        print(f"⚠️ Erreur lecture config : {e}")
        return None

def locate_image(filename, confidence=0.7):
    path = os.path.join(IMAGE_PATH, filename)
    try:
        return pyautogui.locateCenterOnScreen(path, confidence=confidence)
    except Exception as e:
        print(f"⚠️ Erreur locate {filename} : {e}")
        return None

def click_location(location, delay):
    if location:
        pyautogui.moveTo(location)
        pyautogui.click()
        time.sleep(delay)

def wait_for_avatar(delay, max_misses=1):
    misses = 0
    while True:
        if locate_image("avatar.png"):
            return True
        misses += 1
        if misses >= max_misses:
            return False
        time.sleep(delay)

def est_ton_tour(delay=0.3):
    return locate_image("autorisation_attack.png", confidence=0.85) is not None

def do_turn(mode, coords, delay, spell_key):
    # Lancer 1er sort + clic
    pyautogui.press(spell_key)
    time.sleep(delay)
    target = locate_image("mob.png") if mode == "1" else coords
    if target:
        pyautogui.moveTo(target)
        pyautogui.click()
        time.sleep(delay)

    # Lancer 2e sort + clic (même sort)
    pyautogui.press(spell_key)
    time.sleep(delay)
    if target:
        pyautogui.moveTo(target)
        pyautogui.click()
        time.sleep(delay)

    # Puis passer le tour
    pyautogui.press("f1")
    time.sleep(delay)


def wait_for_combat_start(delay, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        if locate_image("avatar.png"):
            return True
        time.sleep(delay)
    return False

def post_combat_cleanup(delay):
    print("🔚 Fin combat – nettoyage")
    for _ in range(2):
        pyautogui.press("enter")
        time.sleep(0.1)

    wait_start = time.time()
    while time.time() - wait_start < 10:
        mob = locate_image("mob.png")
        pret = locate_image("pret.png")
        if mob or pret:
            return
        time.sleep(0.5)
    print("⏳ Rien détecté après 10s, on continue quand même.")

def fight_loop(config):
    mode = config["mode"]
    coords = config["coords"]
    delay = config["delay"]
    spell_key = config["spell_key"]
    alt_spell_key = config["alt_spell_key"]

    # Attente du bouton prêt
    while not locate_image("pret.png"):
        time.sleep(delay)

    pyautogui.press("f1")
    time.sleep(delay * 2)

    # Attente du début réel du combat
    if not wait_for_combat_start(delay):
        print("⚠️ Combat non lancé après prêt.")
        return

    combat_start = time.time()

    for i in range(50):  # 50 tours max
        if not wait_for_avatar(delay, max_misses=5):
            print("✅ Avatar disparu → combat terminé.")
            post_combat_cleanup(delay)
            return

        elapsed = time.time() - combat_start
        print(f"🕐 Tour {i+1} | Temps écoulé : {elapsed:.1f}s")

        # Vérifie si c’est bien le tour du personnage principal (absence de l'image autorisation_attack)
        autorisation = locate_image("autorisation_attack.png", confidence=0.9)
        if autorisation is not None:
            # C’est le tour du joueur principal, on attaque
            if elapsed > 10 and i >= 2:
                print("⚔️ Combat long → sort alternatif")

                # 1er lancement sort alternatif + clic
                pyautogui.press(alt_spell_key)
                time.sleep(delay)
                target = locate_image("mob.png") if mode == "1" else coords
                if target:
                    pyautogui.moveTo(target)
                    pyautogui.click()
                    time.sleep(delay)

                # 2e lancement sort alternatif + clic
                pyautogui.press(alt_spell_key)
                time.sleep(delay)
                if target:
                    pyautogui.moveTo(target)
                    pyautogui.click()
                    time.sleep(delay)

                # Puis passer le tour
                pyautogui.press("f1")
                time.sleep(delay)
                time.sleep(delay)
            else:
                do_turn(mode, coords, delay, spell_key)
        else:
            # Ce n’est pas son tour → passe son tour avec F1
            print("⏭️ Pas son tour → passe avec F1")
            pyautogui.press("f1")
            time.sleep(delay)

    print("🔁 Fin boucle combat (50 tours atteints)")
    post_combat_cleanup(delay)


def main():
    while True:
        config = load_config()
        if not config:
            time.sleep(1)
            continue

        mob = locate_image("mob.png")
        if mob:
            click_location(mob, config["delay"])
            time.sleep(config["delay"])

            if not wait_for_avatar(config["delay"], max_misses=5):
                continue

            fight_loop(config)
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    main()
