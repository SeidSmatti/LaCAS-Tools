# SimpleWhisper (Version Archivée)

Un outil de transcription facile à manier utilisant la bibliothèque [faster-whisper](https://github.com/SYSTRAN/faster-whisper), optimisant les performances des modèles [Whisper](https://github.com/openai/whisper) pour la transcription sur CPU et GPU.

**À noter :** Cette version de SimpleWhisper est archivée. La version en cours de développement est disponible à l'adresse suivante : [https://github.com/SeidSmatti/SimpleWhisper](https://github.com/SeidSmatti/SimpleWhisper).

SimpleWhisper a été développé dans le cadre du [Projet LaCAS](https://lacas.inalco.fr/le-projet-lacas) pour [l'INALCO](https://www.inalco.fr/) (Institut National des Langues et Civilisations Orientales).

## Méthode et Résultats

### Méthode

La bibliothèque faster-whisper, développée par SYSTRAN, propose un système de reconnaissance automatique de la parole (ASR) optimisé et efficace. Bien que Whisper offre des capacités puissantes, son utilisation via la ligne de commande et sa configuration technique peuvent constituer une barrière pour de nombreux utilisateurs. SimpleWhisper résout ce problème en fournissant une interface graphique (GUI) qui simplifie l'utilisation du modèle Whisper, permettant aux utilisateurs de transcrire facilement des fichiers audio ou vidéo.

**Caractéristiques principales :**
- **Chargement des modèles :** Possibilité de charger différents modèles Whisper selon les besoins.
- **Conversion audio :** Conversion des fichiers vidéo en format audio avec `ffmpeg`.
- **Transcription :** Transcription des fichiers audio avec ou sans codes temporels.
- **Accélération GPU :** Utilisation de CUDA pour accélérer la transcription si un GPU est disponible.

## Instructions d'exécution

### Prérequis

- Python 3.7 ou supérieur
- `ffmpeg` installé et disponible dans le PATH.
- `tkinter` installé.
- Pour l'accélération GPU (facultatif), assurez-vous que CUDA est installé. Consultez le [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) pour les instructions d'installation.

[Tutoriels d'installation de FFMPEG](https://gist.github.com/barbietunnie/47a3de3de3274956617ce092a3bc03a1) 

### Installation

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/SeidSmatti/SimpleWhisper.git
    cd SimpleWhisper
    ```

2. Créez un environnement virtuel (facultatif) :
    ```sh
    python -m venv venv
    source venv/bin/activate  # Sur Windows : `venv\Scripts\activate`
    ```

3. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```
4. Installez tkinter

   Pour Mac OS
   ```sh
   brew install python-tk
   ```

   Pour Linux (basé sur Debian)
   ```sh
   sudo apt-get install python3-tk
   ```

   Pour Windows

   Normalement préinstallé avec Python. Sinon, consultez la [documentation officielle](https://tkdocs.com/tutorial/install.html).

**Remarque :** Pour Windows, vous pouvez directement télécharger le binaire (non signé pour l'instant) depuis la page [Releases](https://github.com/SeidSmatti/SimpleWhisper/releases).

### Utilisation

1. Lancez l'application :
    ```sh
    python src/main.py
    ```

2. Sinon, installez le package et utilisez le point d'entrée :
    ```sh
    pip install .
    simplewhisper
    ```

### Fonctionnalités

- Chargement des fichiers audio ou vidéo (avec conversion automatique).
- Choix de la mise en forme de la sortie.
- Possibilité de choisir entre l'utilisation du modèle sur CPU ou GPU.

### Tests

Exécutez les tests unitaires pour vérifier que tout fonctionne correctement :
```sh
python -m unittest discover -s tests
```

## Ressources Supplémentaires

Pour plus d'informations sur Whisper, faster-whisper et CUDA :
- [Open-AI Whisper](https://github.com/openai/whisper)
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)

## Additions 
- **22/07/2024 :** Ajout de la sélection manuelle de la langue.
- **17/09/2024 :** Mise en cache des modèles pour un chargement plus rapide, interface graphique réactive avec gestion améliorée des threads, gestion sécurisée des fichiers temporaires, meilleure gestion des erreurs, refactorisation du code (modularisation et lisibilité), unification de la gestion des langues et optimisation des performances selon la configuration de l'appareil.

## À propos

SimpleWhisper a été initialement développé dans le cadre du projet LaCAS pour l'INALCO (Institut National des Langues et Civilisations Orientales). Le projet vise à rendre les technologies avancées de transcription accessibles à un public plus large.

Ce projet fait partie des efforts collaboratifs de l'équipe LaCAS pour faire progresser les études aréales à travers des solutions technologiques innovantes.

