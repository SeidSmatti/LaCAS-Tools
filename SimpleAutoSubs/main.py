import os
import threading
import tempfile
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from transcriber import transcribe_audio, convert_to_audio, write_transcriptions_to_file
from embedder import convert_to_srt, embed_subtitles

# Pour éviter les conflits liés aux bibliothèques de traitement parallèle
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Fonction pour enregistrer des messages dans la zone de log
def log(message):
    log_box.insert(ctk.END, message + "\n")  # Ajoute le message à la fin de la zone de texte
    log_box.see(ctk.END)  # Fait défiler automatiquement vers le bas

# Fonction pour parcourir et sélectionner un fichier
def browse_file(entry):
    file_path = filedialog.askopenfilename()  # Ouvre une boîte de dialogue pour sélectionner un fichier
    if file_path:
        entry.delete(0, ctk.END)  # Efface le contenu actuel de l'entrée
        entry.insert(0, file_path)  # Insère le chemin du fichier sélectionné

# Fonction pour parcourir et sélectionner un fichier de sortie
def browse_output(entry):
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])  # Fichier de sortie MP4
    if output_path:
        entry.delete(0, ctk.END)  # Efface le contenu actuel de l'entrée
        entry.insert(0, output_path)  # Insère le chemin du fichier sélectionné

# Démarre la transcription dans un thread séparé pour éviter de bloquer l'interface utilisateur
def start_transcription_thread():
    threading.Thread(target=start_transcription).start()

# Processus de transcription
def start_transcription():
    input_file = file_entry.get()  # Chemin du fichier d'entrée
    model_size = model_size_var.get()  # Taille du modèle
    device = "cuda" if gpu_var.get() else "cpu"  # Utilise le GPU si sélectionné, sinon CPU
    include_timecodes = timecodes_var.get()  # Inclure les codes temporels ou non
    selected_language = language_var.get()  # Langue sélectionnée
    
    # Vérification des champs obligatoires
    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return
    output_file = output_entry.get()
    if not output_file:
        messagebox.showerror("Error", "Please select an output file.")
        return

    # Gère les fichiers audio et vidéo
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = os.path.join(temp_dir, "temp_audio.wav")
        if input_file.endswith(('.mp4', '.mkv', '.avi')):
            log("Converting video to audio...")
            convert_to_audio(input_file, audio_path)  # Convertit la vidéo en audio
        else:
            audio_path = input_file  # Si déjà un fichier audio, pas de conversion nécessaire

        # Transcrit l'audio
        transcriptions = transcribe_audio(model_size, device, audio_path, include_timecodes, log, selected_language)

        # Sauvegarde la transcription dans un fichier
        write_transcriptions_to_file(transcriptions, output_file)

    # Affiche la transcription dans la zone de texte pour édition
    transcription_textbox.delete("1.0", ctk.END)
    transcription_textbox.insert(ctk.END, "\n".join(transcriptions))

# Démarre l'intégration des sous-titres dans un thread séparé
def start_embedding_thread():
    threading.Thread(target=start_embedding).start()

# Fonction pour essayer de supprimer un fichier temporaire
def try_delete_file(file_path, retries=5, delay=1):
    """Essaie de supprimer un fichier avec plusieurs tentatives."""
    for _ in range(retries):
        try:
            os.remove(file_path)
            return
        except PermissionError:
            time.sleep(delay)
    log(f"Could not delete temporary SRT file after multiple attempts. It might still be in use: {file_path}")

# Processus d'intégration des sous-titres
def start_embedding():
    input_text = transcription_textbox.get("1.0", ctk.END).strip()  # Récupère le texte de la transcription
    input_video = file_entry.get()  # Chemin du fichier vidéo d'entrée
    output_video = output_entry.get()  # Chemin du fichier vidéo de sortie

    # Vérification des champs obligatoires
    if not input_text or not input_video or not output_video:
        messagebox.showerror("Error", "Please ensure all fields are filled.")
        return

    # Création d'un fichier temporaire pour les sous-titres
    with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as temp_srt:
        convert_to_srt(input_text, temp_srt.name, log)  # Convertit le texte en sous-titres SRT
        try:
            embed_subtitles(input_video, output_video, temp_srt.name, log)  # Intègre les sous-titres dans la vidéo
        finally:
            threading.Thread(target=try_delete_file, args=(temp_srt.name,)).start()  # Supprime le fichier temporaire

# Configuration de l'interface graphique
ctk.set_appearance_mode("dark")  # Mode sombre
ctk.set_default_color_theme("blue")  # Thème bleu par défaut

# Création de la fenêtre principale
root = ctk.CTk()
root.title("SimpleAutoSubs")

# Configuration des widgets
frame = ctk.CTkFrame(root)
frame.grid(row=0, column=0, padx=20, pady=20)

# Champs pour le fichier d'entrée
ctk.CTkLabel(frame, text="Input File:").grid(row=0, column=0, sticky="w", pady=5)
file_entry = ctk.CTkEntry(frame, width=400)
file_entry.grid(row=0, column=1, padx=5, pady=5)
ctk.CTkButton(frame, text="Browse", command=lambda: browse_file(file_entry)).grid(row=0, column=2, padx=5, pady=5)

# Champs pour le fichier de sortie
ctk.CTkLabel(frame, text="Output File:").grid(row=1, column=0, sticky="w", pady=5)
output_entry = ctk.CTkEntry(frame, width=400)
output_entry.grid(row=1, column=1, padx=5, pady=5)
ctk.CTkButton(frame, text="Browse", command=lambda: browse_output(output_entry)).grid(row=1, column=2, padx=5, pady=5)

# Paramètres de transcription
ctk.CTkLabel(frame, text="Model Size:").grid(row=2, column=0, sticky="w", pady=5)
model_size_var = ctk.StringVar(value="base")
ctk.CTkComboBox(frame, variable=model_size_var, values=["base", "small", "medium", "large", "large-v2", "large-v3"]).grid(row=2, column=1, padx=5, pady=5)

# Sélection de la langue
ctk.CTkLabel(frame, text="Language:").grid(row=3, column=0, sticky="w", pady=5)
language_var = ctk.StringVar(value="autodetect")
supported_languages = [
    # Liste des langues supportées (code, nom)
]
language_options = [label for code, label in supported_languages]
ctk.CTkComboBox(frame, variable=language_var, values=language_options).grid(row=3, column=1, padx=5, pady=5)

# Options avancées
gpu_var = ctk.BooleanVar()
ctk.CTkCheckBox(frame, text="Use GPU", variable=gpu_var).grid(row=4, column=0, sticky="w", padx=5, pady=5)

timecodes_var = ctk.BooleanVar()
ctk.CTkCheckBox(frame, text="Include Timecodes", variable=timecodes_var).grid(row=4, column=1, sticky="w", padx=5, pady=5)

# Boutons d'action
ctk.CTkButton(frame, text="Start Transcription", command=start_transcription_thread).grid(row=5, column=0, columnspan=3, pady=10)
transcription_textbox = ctk.CTkTextbox(frame, height=200, width=600)
transcription_textbox.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

ctk.CTkButton(frame, text="Embed Subtitles", command=start_embedding_thread).grid(row=7, column=0, columnspan=3, pady=10)

log_box = ctk.CTkTextbox(frame, height=100, width=600)
log_box.grid(row=8, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

# Lancement de la boucle principale de l'application
root.mainloop()

