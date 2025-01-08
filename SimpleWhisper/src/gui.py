import customtkinter as ctk
from tkinter import filedialog, messagebox
from transcriber import model_manager, convert_to_audio, transcribe_audio, set_log_box, log, write_transcriptions_to_file
import threading
import os
from languages import supported_languages

# Fonction principale pour lancer l'interface graphique
def start_gui():
    # Gestion de la sélection du fichier d'entrée
    def browse_file():
        file_path = filedialog.askopenfilename()  # Ouvre une boîte de dialogue pour sélectionner un fichier
        if file_path:
            file_entry.delete(0, ctk.END)  # Efface l'entrée actuelle
            file_entry.insert(0, file_path)  # Insère le chemin du fichier sélectionné

    # Gestion de la sélection du fichier de sortie
    def browse_output():
        output_path = filedialog.asksaveasfilename(defaultextension=".txt")  # Ouvre une boîte de dialogue pour choisir où sauvegarder
        if output_path:
            output_entry.delete(0, ctk.END)  # Efface l'entrée actuelle
            output_entry.insert(0, output_path)  # Insère le chemin du fichier de sortie

    # Lancement de la transcription dans un thread séparé pour éviter de bloquer l'interface graphique
    def start_transcription_thread():
        start_button.configure(state='disabled')  # Désactive le bouton pendant l'exécution
        threading.Thread(target=start_transcription).start()  # Exécute la transcription en arrière-plan

    # Processus de transcription principal
    def start_transcription():
        try:
            # Récupération des valeurs saisies par l'utilisateur
            input_file = file_entry.get()
            output_file = output_entry.get()
            model_size = model_size_var.get()
            device = "cuda" if gpu_var.get() else "cpu"  # Utilise le GPU si disponible, sinon CPU
            include_timecodes = timecodes_var.get()
            selected_language_label = language_var.get()

            # Vérification que les fichiers d'entrée et de sortie ont été fournis
            if not input_file or not output_file:
                messagebox.showerror("Error", "Veuillez sélectionner un fichier d'entrée et un fichier de sortie.")
                return

            # Chargement du modèle Whisper selon la taille et le périphérique sélectionnés
            model = model_manager.load_model(model_size, device, "int8" if device == "cpu" else "float16")

            # Conversion du fichier vidéo en audio si nécessaire
            if input_file.endswith(('.mp4', '.mkv', '.avi')):
                log("Conversion de la vidéo en audio...")
                audio_path = convert_to_audio(input_file)
                temp_audio = True  # Indique qu'un fichier temporaire est créé
            else:
                audio_path = input_file
                temp_audio = False

            # Transcription de l'audio avec les options sélectionnées
            transcriptions = transcribe_audio(model, audio_path, include_timecodes, selected_language_label)

            # Sauvegarde des transcriptions dans le fichier de sortie
            write_transcriptions_to_file(transcriptions, output_file)

            # Suppression des fichiers audio temporaires s'ils ont été créés
            if temp_audio and os.path.exists(audio_path):
                os.remove(audio_path)

            log("Transcription terminée avec succès.")
        except Exception as e:
            log(f"Une erreur est survenue pendant la transcription : {e}")
        finally:
            # Réactivation du bouton une fois la transcription terminée
            root.after(0, lambda: start_button.configure(state='normal'))

    # Configuration de l'apparence et du thème de l'interface graphique
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Création de la fenêtre principale
    root = ctk.CTk()
    root.title("SimpleWhisper Transcription Tool")

    # Ajout des widgets (champs, boutons, menus déroulants) pour l'interface utilisateur
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Champs pour le fichier d'entrée
    ctk.CTkLabel(frame, text="Input File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    file_entry = ctk.CTkEntry(frame, width=400)
    file_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    ctk.CTkButton(frame, text="Browse", command=browse_file).grid(row=0, column=2, sticky="w", padx=5, pady=5)

    # Champs pour le fichier de sortie
    ctk.CTkLabel(frame, text="Output File:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    output_entry = ctk.CTkEntry(frame, width=400)
    output_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    ctk.CTkButton(frame, text="Browse", command=browse_output).grid(row=1, column=2, sticky="w", padx=5, pady=5)

    # Sélection de la taille du modèle
    ctk.CTkLabel(frame, text="Model Size:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    model_size_var = ctk.StringVar(value="base")
    ctk.CTkComboBox(
        frame,
        variable=model_size_var,
        values=["base", "small", "medium", "large", "large-v2", "large-v3"]
    ).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    # Sélection de la langue pour la transcription
    ctk.CTkLabel(frame, text="Language:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    language_var = ctk.StringVar(value="Autodetect")
    language_options = [label for code, label in supported_languages]
    ctk.CTkComboBox(frame, variable=language_var, values=language_options).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

    # Options pour utiliser le GPU et inclure les codes temporels
    gpu_var = ctk.BooleanVar()
    ctk.CTkCheckBox(frame, text="Use GPU", variable=gpu_var).grid(row=4, column=0, sticky="w", padx=5, pady=5)

    timecodes_var = ctk.BooleanVar()
    ctk.CTkCheckBox(frame, text="Include Timecodes", variable=timecodes_var).grid(row=4, column=1, sticky="w", padx=5, pady=5)

    # Bouton pour démarrer la transcription
    start_button = ctk.CTkButton(frame, text="Start Transcription", command=start_transcription_thread)
    start_button.grid(row=5, column=0, columnspan=3, pady=10)

    # Zone de texte pour afficher les journaux et les messages
    log_box = ctk.CTkTextbox(frame, height=200, width=600)
    log_box.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

    set_log_box(log_box)  # Associe la zone de texte aux journaux de transcription

    # Lancement de la boucle principale de l'interface graphique
    root.mainloop()

