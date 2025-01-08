# SimpleAutoSubs (Version Archivée)

SimpleAutoSubs est un outil permettant de transcrire et d’intégrer des sous-titres dans des vidéos en utilisant [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) et [FFmpeg](https://ffmpeg.org/). Cet outil offre une interface graphique (GUI) simple d’utilisation pour transcrire des vidéos et y intégrer les sous-titres de manière transparente.

**À noter :** Cette version de SimpleAutoSubs est archivée. La version en cours de développement est disponible ici : [SeidSmatti/SimpleAutoSubs](https://github.com/SeidSmatti/SimpleAutoSubs).

SimpleAutoSubs a été développé dans le cadre du [Projet LaCAS](https://lacas.inalco.fr/le-projet-lacas) pour [l'INALCO](https://www.inalco.fr/) (Institut National des Langues et Civilisations Orientales).

## Fonctionnalités

- Prend en charge les fichiers .mp4, .mkv et .avi.
- Génère et intègre des sous-titres dans les fichiers vidéo.
- Supporte l’accélération GPU.

## Installation

### Prérequis

- Python 3.7 ou version ultérieure
- FFmpeg
- CUDA Toolkit (pour l’accélération GPU) 
  - **Remarque :** Actuellement, Faster Whisper ne supporte que CUDA 11.x.

Consultez les instructions d'installation ici : [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit).

[Tutoriels d'installation de FFMPEG](https://gist.github.com/barbietunnie/47a3de3de3274956617ce092a3bc03a1)

### Étapes

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/SeidSmatti/SimpleAutoSubs.git
    cd SimpleAutoSubs
    ```

2. Créez un environnement virtuel et activez-le (optionnel mais recommandé) :
    ```sh
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances requises :
    ```sh
    pip install -r requirements.txt
    ```

4. Installez tkinter :

   - **Pour macOS** :
     ```sh
     brew install python-tk
     ```

   - **Pour Linux (Debian et dérivés)** :
     ```sh
     sudo apt-get install python3-tk
     ```

   - **Pour Windows** :
     Tkinter est habituellement préinstallé avec Python. Sinon, consultez la [documentation officielle](https://tkdocs.com/tutorial/install.html).

## Utilisation

Exécutez le script principal :
```sh
python main.py
```

### Aperçu de l'interface graphique

1. **Fichier d'entrée** : Sélectionnez le fichier vidéo à transcrire. (Si le format n’est pas supporté, utilisez `ffmpeg -i sourcefile.ext newfile.mp4`.)
2. **Fichier de sortie** : Sélectionnez l’emplacement pour enregistrer la vidéo finale avec sous-titres.
3. **Taille du modèle** : Choisissez la taille du modèle Whisper.
4. **Utiliser le GPU** : Activez cette option pour l’accélération GPU.
5. **Inclure les codes temporels** : Cochez cette case, sauf si vous souhaitez uniquement une transcription propre sans sous-titres. (Dans ce cas, nous recommandons [SimpleWhisper](https://github.com/SeidSmatti/SimpleWhisper).)
6. **Démarrer la transcription** : Cliquez sur ce bouton pour lancer le processus de transcription. (Vous pouvez corriger les erreurs dans la zone de texte avant d’intégrer les sous-titres.)
7. **Intégrer les sous-titres** : Cliquez sur ce bouton pour intégrer les sous-titres générés dans la vidéo.

## Ressources supplémentaires

Pour plus d’informations sur Whisper, Faster Whisper et CUDA :
- [Open-AI Whisper](https://github.com/openai/whisper)
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)


## Licence

Ce projet est sous licence GNU General Public License. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

