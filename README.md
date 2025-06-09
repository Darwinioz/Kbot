
# ⚔️ Bot Dofus — Combats & Farming de Donjon Automatisés

Bienvenue dans **Bot Dofus**, un script Python complet pour automatiser les combats et le farming dans **Dofus Retro** et **Dofus 2.0**. Ce bot propose deux modules :

- 🤖 **Mode Combat** : gère les combats en boucle avec reconnaissance d'image.
- 🗺️ **Mode Donjon** : automatise les combats dans des donjons multi-salles avec configuration fine.

---

## 🚀 Fonctionnalités

- Compatibilité **Dofus Retro** et **Dofus 2.0**
- Interface graphique intuitive (CustomTkinter)
- Deux modules indépendants :
  - **Combat général** (clics, sorts, reconnaissance d'écran)
  - **Farming de donjon** (multi-salles, mouvements, cibles)
- Sauvegarde automatique des configurations (`.txt` et `.json`)
- Reconnaissance visuelle des mobs, boutons, avatars
- Support des sorts principaux/alternatifs, gestion de la latence

---

## 🧠 Modules Disponibles

### 🤖 Mode Combat (main.py)

Configuration via `config.txt` :

```
retro
1
512,433
0.5
p
m
on
```

- **Version** : `retro` ou `2.0`
- **Mode** : `1` (attaque directe) ou `2` (attaque une case)
- **Coordonnées** : `x,y` (requis si mode `2`)
- **Latence** : délai entre actions (ex. `0.5` secondes)
- **Sort principal** / **alternatif** : touches clavier (ex. `p`, `m`)
- **État** : `on` ou `off`

---

### 🗺️ Mode Donjon (main_donjon.py)

Configuration via `config_donjon.json` :

```json
{
  "nb_salles": 3,
  "salles": [
    {
      "mode": "2",
      "coords": [1545, 400],
      "move_enabled": false,
      "move_coords": [0, 0]
    },
    {
      "mode": "1",
      "coords": [],
      "move_enabled": true,
      "move_coords": [760, 750]
    },
    {
      "mode": "3",
      "coords": [],
      "move_enabled": false,
      "move_coords": [0, 0]
    }
  ]
}
```

- **mode** : `"1"` (attaque directe), `"2"` (clic sur une case), `"3"` (mode personnalisé)
- **coords** : coordonnées de ciblage (obligatoire en mode 2)
- **move_enabled** : déplacement activé en début de combat
- **move_coords** : coordonnées de déplacement

---

## 🖥️ Interface Graphique

Lancer l’interface avec :

```bash
python interface.py
```

Fonctionnalités :
- Sélection du mode (combat ou donjon)
- Choix du nombre de salles (mode donjon)
- Configuration par salle : mode, cibles, déplacements
- Lancement / arrêt du bot via boutons

---

## 🔍 Fonctionnement (Combat)

1. Recherche d’image `mob.png` à l’écran (via OpenCV)
2. Si trouvé → clic sur le mob
3. Attente de `pret.png`, puis appui sur **Espace**
4. Lancement du combat :
   - Sort principal / alternatif
   - Clic sur la cible ou case
   - Appui sur **Espace**
5. Fin de combat → détection de disparition de `avatar.png`
6. Fermeture des pop-ups via **Entrée**

---

## 💡 Astuce : Personnaliser les Mobs avec un .SWF

Dans le dossier `/images`, un fichier `template.swf` sert de base pour détecter les monstres.

> ✨ **Astuce** : Si tu veux farmer un monstre spécifique, remplace `template.swf` par un export `.swf` du mob ciblé. Renomme simplement ton fichier en `template.swf`, et place-le dans le dossier `/images`. Cela permet d’améliorer la détection par reconnaissance.

---

## 📁 Arborescence du Projet

```
BotDofus/
├── config.txt
├── config_donjon.json
├── demarrage.bat
├── donjon_utils.py
├── interface.py
├── logo.png
├── main.py
├── main2.py
├── main_donjon.py
├── README.md
├── requirements.txt
├── __pycache__/
├── utils/
└── images/
    ├── mob.png
    ├── pret.png
    ├── avatar.png
    ├── template.swf
    ├── parler.png
    ├── pnj_entree.png
    ├── pnj_sortie.png
    ├── autorisation_attack.png
    ├── levelup.png
    ├── bouton_x.png
    ├── puissance.png
    ├── sortir.png
    ├── tremblement.png
    ├── vent.png
    ├── retro/
    └── dofus2/
```

---

## 📦 Dépendances

Créer un environnement virtuel (optionnel mais recommandé) puis installe les paquets nécessaires :

```bash
pip install -r requirements.txt
```

Contenu recommandé de `requirements.txt` :

```
pyautogui
opencv-python
pytesseract
Pillow
keyboard
tk
customtkinter
```

⚠️ Assure-toi que **Tesseract OCR** est bien installé sur ton système.

---

## 📬 Support

Pour toute question, suggestion ou bug :
- 📧 [TonNomOuMail]
- 🐙 Ouvre une issue sur GitHub

---

Merci d’utiliser **Bot Dofus** !  
🧪 Bon farm, bon drop et à bientôt dans le Monde des Douze 🎮🐉
