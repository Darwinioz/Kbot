import pyautogui
import time
import os
import cv2
import numpy as np


CONFIG_PATH = "config.txt"
IMAGE_PATH = os.path.join("images", "retro")

pyautogui.USE_IMAGE_NOT_FOUND_EXCEPTION = False

def load_config():
    """
    Lit config.txt et renvoie un dictionnaire avec :
      - version, mode, coords, delay, spell_key, alt_spell_key,
      - move_enabled (bool), move_coords (tuple)
    Si config.txt est incomplet, on complète avec des valeurs par défaut.
    """
    # Valeurs par défaut si lignes manquantes
    defaults = [
        "retro",    # version
        "1",        # mode
        "512,433",  # coords
        "0.5",      # delay
        "p",        # spell_key
        "m",        # alt_spell_key
        "on",       # etat
        "off",      # move_enabled
        "400,400"   # move_coords
    ]

    try:
        # Si le fichier n'existe pas, on le crée avec les valeurs par défaut
        if not os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "w") as f:
                f.write("\n".join(defaults) + "\n")
            lines = defaults.copy()
        else:
            # Lit toutes les lignes existantes
            with open(CONFIG_PATH, "r") as f:
                lines = f.read().splitlines()
            # Complète si moins de 9 lignes
            while len(lines) < 9:
                lines.append(defaults[len(lines)])

        # Maintenant lines a au moins 9 éléments
        version       = lines[0].strip()
        mode          = lines[1].strip()
        coords_str    = lines[2].strip()
        delay         = float(lines[3].strip())
        spell_key     = lines[4].strip()
        alt_spell_key = lines[5].strip()
        etat          = lines[6].strip().lower()
        move_enabled  = (lines[7].strip().lower() == "on")
        move_coords   = tuple(map(int, lines[8].split(","))) if "," in lines[8] else (400, 400)

        # Si etat = "off", on considère que le bot est désactivé
        if etat == "off":
            print("⛔ Bot désactivé via config.txt")
            return None

        # Transforme coords_str en tuple (x, y)
        if "," in coords_str:
            x, y = map(int, coords_str.split(","))
            coords = (x, y)
        else:
            # Valeur invalide, on met une valeur par défaut
            coords = (512, 433)

        return {
            "version": version,
            "mode": mode,
            "coords": coords,
            "delay": delay,
            "spell_key": spell_key,
            "alt_spell_key": alt_spell_key,
            "move_enabled": move_enabled,
            "move_coords": move_coords
        }

    except Exception as e:
        print(f"⚠️ Erreur lecture config : {e}")
        return None


def locate_image(filename, confidence=0.80):
    """
    Recherche d'une image à l'écran via OpenCV (plus précis que pyautogui).
    Renvoie les coordonnées du centre de l'image trouvée ou None.
    """
    path = os.path.join(IMAGE_PATH, filename)

    try:
        # Capture l'écran et convertit en format OpenCV
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Charge et convertit le template
        template = cv2.imread(path)
        if template is None:
            print(f"❌ Image de template introuvable : {filename}")
            return None

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            center_x = max_loc[0] + template.shape[1] // 2
            center_y = max_loc[1] + template.shape[0] // 2
            print(f"✅ Image trouvée : {filename} à ({center_x}, {center_y}) (score={max_val:.2f})")
            return (center_x, center_y)
        else:
            print(f"❌ Image NON trouvée : {filename} (score={max_val:.2f}, attendu ≥ {confidence})")
            return None

    except Exception as e:
        print(f"⚠️ Erreur locate {filename} : {e}")
        return None        

def click_location(location, delay):
    """
    Déplace la souris vers location et clique, puis attend 'delay' secondes.
    """
    if location:
        pyautogui.moveTo(location)
        pyautogui.click()
        time.sleep(delay)

def wait_for_avatar(delay, max_misses=1):
    """
    Attend l'apparition de avatar.png (début de tour).
    Si ce n'est pas détecté après 'max_misses' tentatives, renvoie False.
    """
    misses = 0
    while True:
        if locate_image("avatar.png"):
            return True
        misses += 1
        if misses >= max_misses:
            return False
        time.sleep(delay)

def do_turn(mode, coords, delay, spell_key):
    """
    Exécute un tour normal (2 lancers du même sort puis 'F1').
    """
    if mode == "3":
        return

    # Premier sort
    pyautogui.press(spell_key)
    time.sleep(delay)

    # Cibler
    if mode == "1":
        target = locate_image("mob.png")
    else:
        target = coords

    if target:
        pyautogui.moveTo(target)
        pyautogui.click()
        time.sleep(delay)

    # Deuxième sort
    pyautogui.press(spell_key)
    time.sleep(delay)

    # 🔁 Mettre à jour la cible si mode 1 (mob possiblement mort)
    if mode == "1":
        target = locate_image("mob.png")

    if target:
        pyautogui.moveTo(target)
        pyautogui.click()
        time.sleep(delay)

    # Fin de tour
    pyautogui.press("F1")
    time.sleep(delay)

def do_turn_sadida_fourbe(delay):
    """
    Lance successivement 3 sorts Sadida avec clic droit sur leurs icônes :
      - tremblement.png
      - vent.png
      - puissance.png
    Puis passe le tour.
    """
    # 1) Tremblement
    tremblement = locate_image("tremblement.png", confidence=0.8)
    if tremblement:
        pyautogui.moveTo(tremblement)
        pyautogui.click(button="right")
        time.sleep(delay)

    # 2) Vent Empoisonné
    vent = locate_image("vent.png", confidence=0.8)
    if vent:
        pyautogui.moveTo(vent)
        pyautogui.click(button="right")
        time.sleep(delay)

    # 3) Puissance Sylvestre
    puissance = locate_image("puissance.png", confidence=0.8)
    if puissance:
        pyautogui.moveTo(puissance)
        pyautogui.click(button="right")
        time.sleep(delay)

    # Enfin, on passe le tour
    pyautogui.press("F1")
    time.sleep(delay)

def wait_for_combat_start(delay, timeout=15):
    """
    Après avoir cliqué sur le mob et appuyé sur 'F1' pour 'prêt',
    on attend que l'avatar apparaisse à l'écran, signe que le combat démarre.
    """
    start = time.time()
    while time.time() - start < timeout:
        if locate_image("avatar.png"):
            return True
        time.sleep(delay)
    return False

def post_combat_cleanup(delay):
    """
    Actions à faire après la fin du combat :
      - Appuyer 2x sur 'enter' (nb : ferme level-up, drop, etc.)
      - Attendre jusqu’à 10s pour vérifier si un nouveau mob ou 'pret.png' apparaît.
      - Si rien en 10s, on continue quand même.
    """
    print("🔚 Fin combat – nettoyage")
    for _ in range(2):
        pyautogui.press("enter")
        time.sleep(0.1)

    wait_start = time.time()
    while time.time() - wait_start < 3:
        mob = locate_image("mob.png")
        pret = locate_image("pret.png")
        if mob or pret:
            return
        time.sleep(0.5)

    print("⏳ Rien détecté après 10s, on continue quand même.")
    


def fight_loop(config):
    """
    Boucle principale pour gérer le déroulé du combat.
    On effectue jusqu'à 50 tours max, ou jusqu'à ce que avatar.png disparaisse.
    Si mode == "3", on appelle do_turn_sadida_fourbe(), sinon do_turn().
    """
    mode          = config["mode"]
    coords        = config["coords"]
    delay         = config["delay"]
    spell_key     = config["spell_key"]
    alt_spell_key = config["alt_spell_key"]
    move_enabled  = config["move_enabled"]
    move_coords   = config["move_coords"]

    # 1) On attend le bouton 'Prêt'
    while not locate_image("pret.png"):
        time.sleep(delay)

    # 2) On appuie sur 'F1' pour démarrer le combat
    pyautogui.press("F1")
    time.sleep(delay * 2)

    # 3) On attend la vraie apparition de l'avatar (début de combat)
    if not wait_for_combat_start(delay):
        print("⚠️ Combat non lancé après prêt.")
        return

    combat_start = time.time()

    # 4) Boucle sur chaque tour (max 50)
    for i in range(50):
        # 4.1) On attend l’affichage de avatar.png pour chaque tour
        if not wait_for_avatar(delay, max_misses=1):
            print("✅ Avatar disparu → combat terminé.")
            post_combat_cleanup(delay)
            return

        # 4.2) Déplacement au 1er tour si activé
        if i == 0 and move_enabled:
            print(f"🚶 Déplacement tour 1 vers {move_coords}")
            pyautogui.moveTo(move_coords)
            pyautogui.click()
            # On laisse un peu de temps au personnage pour se déplacer
            time.sleep(delay * 2)

        elapsed = time.time() - combat_start
        print(f"🕐 Tour {i+1} | Temps écoulé : {elapsed:.1f}s")
        # 4.3) Détection du tour du joueur principal via autorisation_attack.png
        autorisation = locate_image("autorisation_attack.png", confidence=0.90)

        if autorisation is None:
            time.sleep(0.2)  # petite pause entre les deux scans
            autorisation = locate_image("autorisation_attack.png", confidence=0.90)

        if autorisation is not None:            
            if elapsed > 3 :
                print(f"⚔️ Combat long → sort alternatif (mode {mode})")

                # 1er lancement sort alternatif + clic
                pyautogui.press(alt_spell_key)
                time.sleep(delay)

                target = locate_image("mob.png")
                if not target:
                    print("❌ Mob introuvable pour le sort alternatif.")
                if target:
                    pyautogui.moveTo(target)
                    pyautogui.click()
                    time.sleep(delay)

                # 2e lancement → on recalcule la cible
                pyautogui.press(alt_spell_key)
                time.sleep(delay)

                
                target = locate_image("mob.png")  # 🔁 redétection

                if target:
                    pyautogui.moveTo(target)
                    pyautogui.click()
                    time.sleep(delay)
                if not target:
                    print("❌ Mob introuvable pour le sort alternatif.")

                pyautogui.press("F1")
                time.sleep(delay)

            else:
                # Tour normal
                if mode == "3":
                    print("🌿 Mode Sadida Fourbe - lancement des sorts")
                    do_turn_sadida_fourbe(delay)
                else:
                    do_turn(mode, coords, delay, spell_key)

        else:
            print("⏭️ Pas son tour → passe avec F1")
            #pyautogui.press("f1")
            #time.sleep(delay)

    # Si on sort de la boucle (50 tours atteints)
    print("🔁 Fin boucle combat (50 tours atteints)")
    post_combat_cleanup(delay)