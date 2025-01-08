import os
import time
from faster_whisper import WhisperModel
import subprocess
import tempfile
from languages import supported_languages
import sys

log_box = None  
# Détermine le chemin de l'exécutable FFMPEG
def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        # Cas où l'application est compilée en exécutable (PyInstaller)
        bundle_dir = sys._MEIPASS
    else:
        # Cas où l'application est exécutée normalement
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_executable = os.path.join(bundle_dir, 'ffmpeg.exe')
    return ffmpeg_executable

# Associe une zone de texte pour afficher les journaux
def set_log_box(log_widget):
    global log_box
    log_box = log_widget

# Fonction pour afficher les messages de journalisation
def log(message):
    if log_box:
        # Si une zone de texte est configurée, y insérer le message
        log_box.insert("end", message + "\n")
        log_box.see("end")
    else:
        # Sinon, afficher le message dans la console
        print(message.encode('utf-8', errors='replace').decode('utf-8'))

# Gestionnaire de modèles Whisper
class ModelManager:
    def __init__(self):
        self.model = None  # Modèle chargé
        self.model_size = None  # Taille du modèle
        self.device = None  # Périphérique (CPU/GPU)
        self.compute_type = None  # Type de calcul (int8, float16, etc.)

    # Charge un modèle Whisper si nécessaire ou réutilise un modèle mis en cache
    def load_model(self, model_size="base", device="cpu", compute_type="int8"):
        # Vérifie si le modèle est déjà chargé avec les mêmes paramètres
        if self.model is None or self.model_size != model_size or self.device != device or self.compute_type != compute_type:
            log(f"Chargement du modèle : size={model_size}, device={device}, compute_type={compute_type}")
            self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
            self.model_size = model_size
            self.device = device
            self.compute_type = compute_type
        else:
            log("Modèle en cache utilisé.")
        return self.model

# Instance unique pour gérer les modèles
model_manager = ModelManager()

# Convertit une vidéo en fichier audio temporaire
def convert_to_audio(input_file):
    try:
        temp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)  # Crée un fichier temporaire
        temp_audio_path = temp_audio_file.name
        temp_audio_file.close()

        ffmpeg_path = get_ffmpeg_path()  # Récupère le chemin vers FFMPEG

        # Commande FFMPEG pour extraire l'audio
        command = [ffmpeg_path, "-y", "-i", input_file, "-q:a", "0", "-map", "a", temp_audio_path]
        subprocess.run(command, check=True)  # Exécute la commande
        return temp_audio_path
    except subprocess.CalledProcessError as e:
        log(f"Erreur lors de la conversion vidéo en audio : {e}")
        raise

# Transcrit un fichier audio en texte
def transcribe_audio(model, audio_path, include_timecodes, language_code):
    try:
        start_time = time.time()
        log(f"Début de la transcription pour {audio_path}")

        # Si la détection automatique de la langue est activée
        if language_code == "autodetect":
            language_code = None

        # Transcription à l'aide du modèle Whisper
        segments, _ = model.transcribe(audio_path, language=language_code)
        transcriptions = []
        for segment in segments:
            start, end, text = segment.start, segment.end, segment.text
            # Ajoute les codes temporels si demandé
            if include_timecodes:
                transcriptions.append(f"{start:.2f}-{end:.2f}: {text}")
            else:
                transcriptions.append(text)

        transcription_time = time.time() - start_time
        log(f"Transcription terminée en {transcription_time:.2f} secondes.")
        return transcriptions
    except Exception as e:
        log(f"Une erreur est survenue : {e}")
        return []

# Écrit les transcriptions dans un fichier de sortie
def write_transcriptions_to_file(transcriptions, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for line in transcriptions:
            file.write(line + '\n')  # Écrit chaque ligne de transcription

