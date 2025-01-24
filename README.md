# retexart

## Description

**retexart** est un outil permettant de retexturer une image en remplaçant les textures originales par des textures fournies par l'utilisateur. Ce projet a pour objectif de faciliter la personnalisation visuelle d'images.

---

## Liste des membres de l’équipe

- **Jérémy Ducourthial**
- **Alexis Feron**

---

## Résumé du projet

Le projet **retexart** repose sur une application de traitement d'images. Grâce à un algorithme performant, il permet de détecter les différentes zones d'une image et de les retexturer en appliquant une texture spécifiée par l'utilisateur. 

Les fonctionnalités principales incluent :
- **Segmentation intelligente** : identification automatique des différentes zones d'une image.
- **Gestion des textures** : possibilité de charger des textures personnalisées pour un rendu unique.
- **Précision et rapidité** : traitement optimisé pour un rendu fidèle et rapide.

---

## Fonctionnalités principales

1. **Chargement des images** : Importez facilement une image depuis votre appareil.
2. **Détection des zones** : L'outil segmente automatiquement les zones pertinentes de l'image.
3. **Application des textures** : Choisissez une texture depuis la bibliothèque intégrée ou importez la vôtre.
4. **Ajustements personnalisés** : Modifiez les paramètres comme l'échelle, l'orientation ou la transparence des textures.
5. **Exportation** : Enregistrez votre image retexturée dans différents formats (PNG, JPG, etc.).

---

## Technologies utilisées

- **Langages** : Python
- **Bibliothèques** :
  - numpy

---

## Installation

### Prérequis

Assurez-vous d'avoir installé :
- Python3

### Étapes

1. Clonez le projet :
   ```bash
   git clone https://github.com/alexis-feron/retexart.git
   cd retexart
   ```

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

3. Lancez le projet :
    ```bash
    python3 app.py
    ```