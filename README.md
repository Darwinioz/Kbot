
# ⚔️ Bot Dofus — Combats & Farming de Donjon Automatisés

Bienvenue dans **KBot**, un script Python complet pour automatiser les combats et le farming dans **Dofus Retro** et **Dofus 2.0 (WIP)**. Ce bot propose deux modules :

- 🤖 **Mode Combat** : gère les combats en boucle avec reconnaissance d'image.
- 🗺️ **Mode Donjon** : automatise les combats dans des donjons multi-salles avec configuration fine.

---
## ❗ DISCLAIMER

Ce projet a un objectif strictement éducatif. Il me permet avant tout de découvrir le langage Python et d’explorer les capacités du modèle 3 de ChatGPT. Je tiens à préciser que je ne cautionne en aucun cas l’utilisation intensive de multi-botting. Cet outil doit plutôt être considéré comme un moyen simple de pallier une courte période d’inactivité, ou encore comme une aide pour les joueurs de Dofus disposant de temps limité, souhaitant progresser sans passer plusieurs heures à farmer devant leur ordinateur.
Je décline toute responsabilité en cas de sanction ou de bannissement, lesquels seraient légitimes au regard des conditions générales d’utilisation de Dofus.

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
1606,767
0.3
p
p
on
off
1080,850 
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

- **mode** : `"1"` (attaque directe), `"2"` (clic sur une case), `"3"` (mode personnalisé type Sadida Fourbe)
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

## 💡 Démonstration

![Demo GIF](https://i.imgur.com/zK0bp2Z.gif)

---


## 💡 Astuce : Personnaliser les Mobs avec un .SWF

Dans le dossier `/images`, un fichier `template.swf` sert de base pour détecter les monstres.

> ✨ **Astuce** : Si tu veux farmer un monstre spécifique, remplace `template.swf` à la place du `.swf` du mob ciblé. Renomme simplement ton fichier `template.swf`, et place-le dans le dossier `/sprites` du jeu. Cela permet d’améliorer la détection par reconnaissance.

---

## 📁 Arborescence du Projet

```
KBot/
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
    ├── retro/
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
    └── dofus2/
	[WIP]
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
- 🐙 Ouvre une issue sur GitHub
---

⚠️ - Vous ne pouvez pas utiliser votre ordinateur pour autre chose pendant que KBOT est en cours d'exécution (utilise la souris et le clavier).

⚠️ - Comme le bot simule un comportement humain normal, vous avez moins de chances d'être repéré par l'Anti-bot.

⚠️ - L'objectif principal de ce bot est de simplifier les tâches répétitives et de réduire l'ennui pendant votre jeu.

⚠️ - **Nous n'encourageons pas le multi-boting et ne le supportons pas de toute façon** (cela détruit l'économie d'un serveur).

🧪 Bon farm, bon drop et à bientôt dans le Monde des Douze 🎮🐉
