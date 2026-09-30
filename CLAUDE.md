# CLAUDE.md — Quittance Tranquille (site de présentation)

Site Hugo (extended **0.121.1**) d'une seule page, qui présente l'outil gratuit `../app` (https://app-quittance.ananse.fr/) avec une vidéo. Tout est en **français**.

## Principes
- Aucun cookie, aucun traceur, aucune ressource externe : la vidéo est servie par le site (`static/video/`).
- **Message n° 1** : aucune donnée n'est envoyée sur un serveur, tout reste sur l'appareil.
- Ne jamais nommer GitHub sur le site ; écrire « service d'hébergement ». Pas de faux avis ni de chiffres inventés.
- Renvoie vers l'outil payant État des lieux Offline (bloc en bas de page).

## Vidéo (`video/`)
```bash
python video/1_voix.py        # voix fr-FR-DeniseNeural (edge-tts) ; « windows » pour la voix hors-ligne
# lancer l'outil : hugo server --source ../app --port 1320
python video/2_capture.py     # filme l'outil au format téléphone
python video/3_montage.py     # -> video/sortie/demo.mp4 + affiche.jpg
python video/4_ecrans.py      # captures d'écran de l'outil -> static/images/ecran-*.jpg
```
Puis copier `video/sortie/demo.mp4` et `affiche.jpg` vers `static/video/`. Le texte est dans `video/scenes.py`.
La synthèse vocale lit mal « par an » en fin de phrase : préférer « l'année ».

## Commandes
- `hugo server` puis http://localhost:1313/quittance-tranquille-decouvrir/
- Déploiement : push sur `main` (workflow GitHub Pages).
