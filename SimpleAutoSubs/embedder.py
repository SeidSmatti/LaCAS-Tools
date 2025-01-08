import os
import re
import subprocess

# Convertit un texte formaté en sous-titres au format SRT
def convert_to_srt(input_text, output_file, log):
    """
    Prend un texte contenant des segments avec des codes temporels et les convertit en fichier SRT.
    
    Args:
        input_text (str): Le texte d'entrée avec les codes temporels (format: start-end: text).
        output_file (str): Le chemin du fichier de sortie SRT.
        log (func): Fonction pour enregistrer les messages de log.
    """
    lines = input_text.split("\n")  # Divise le texte en lignes
    
    with open(output_file, 'w', encoding='utf-8') as srt_file:
        counter = 1  # Compteur de sous-titres
        for line in lines:
            # Vérifie si la ligne correspond au format des sous-titres avec codes temporels
            if re.match(r"^\d+\.\d+-\d+\.\d+:.*$", line):
                time_text = line.split(": ")  # Sépare le code temporel du texte
                times = time_text[0]
                text = time_text[1].strip()
                
                # Divise les temps de début et de fin
                start_time, end_time = times.split('-')
                
                # Formate les temps au format SRT (hh:mm:ss,ms)
                start_time = format_time(float(start_time))
                end_time = format_time(float(end_time))
                
                # Écrit l'entrée de sous-titres dans le fichier SRT
                srt_file.write(f"{counter}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{text}\n\n")
                counter += 1  # Incrémente le compteur
    log(f"Conversion to {output_file} completed\n")  # Log de fin de conversion

# Formate un temps donné en secondes au format SRT (hh:mm:ss,ms)
def format_time(seconds):
    """
    Convertit un temps en secondes en format de temps SRT.
    
    Args:
        seconds (float): Temps en secondes.
        
    Returns:
        str: Temps formaté au format hh:mm:ss,ms.
    """
    millis = int((seconds - int(seconds)) * 1000)  # Extraction des millisecondes
    seconds = int(seconds)
    hours = seconds // 3600  # Calcul des heures
    minutes = (seconds % 3600) // 60  # Calcul des minutes
    seconds = seconds % 60  # Calcul des secondes
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

# Intègre les sous-titres dans une vidéo en utilisant FFmpeg
def embed_subtitles(input_video, output_video, subtitles_file, log):
    """
    Intègre un fichier de sous-titres dans une vidéo à l'aide de FFmpeg.
    
    Args:
        input_video (str): Le chemin de la vidéo d'entrée.
        output_video (str): Le chemin de la vidéo de sortie avec sous-titres.
        subtitles_file (str): Le chemin du fichier de sous-titres SRT.
        log (func): Fonction pour enregistrer les messages de log.
    """
    log(f"Embedding subtitles from {subtitles_file} into {output_video}\n")
    
    # Définit le style des sous-titres pour FFmpeg
    subtitle_style = (
        "FontName=Arial,FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
        "BackColour=&H00000000,Bold=1,Italic=0,BorderStyle=1,Outline=1,Shadow=0,"
        "Alignment=2,MarginV=20"
    )
    
    # Ajuste le format du chemin des sous-titres pour être compatible avec FFmpeg
    subtitles_file = subtitles_file.replace('\\', '/')
    if os.name == 'nt':  # Si l'OS est Windows
        subtitles_file = subtitles_file.replace(':', r'\:')

    # Commande FFmpeg pour intégrer les sous-titres dans la vidéo
    command = [
        'ffmpeg',
        '-i', input_video,  # Vidéo d'entrée
        '-vf', f"subtitles='{subtitles_file}':force_style='{subtitle_style}'",  # Filtre vidéo pour sous-titres
        '-c:a', 'copy',  # Copie le flux audio sans le réencoder
        output_video  # Vidéo de sortie
    ]
    try:
        subprocess.run(command, check=True)  # Exécute la commande FFmpeg
        log(f"Subtitles embedded into {output_video} successfully\n")  # Log de succès
    except subprocess.CalledProcessError as e:
        # Log et levée d'une erreur en cas d'échec
        log(f"Error embedding subtitles: {e}\n")
        raise RuntimeError(f"Error embedding subtitles: {e}")

