import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, font
import requests
import re

# Fonction pour ajouter une URI à la liste
def add_uri():
    uri = uri_entry.get()  # Récupère l'URI saisie
    if uri:  # Si une URI est entrée
        uris.append(uri)  # Ajoute l'URI à la liste
        logbox.insert(tk.END, f"Added URI: {uri}\n")  # Ajoute un message dans la boîte de log
        uri_entry.delete(0, tk.END)  # Efface le champ de saisie

# Fonction pour exécuter une requête SPARQL pour chaque URI
def run_sparql_query():
    result_text.delete('1.0', tk.END)  # Efface le contenu précédent
    for index, uri in enumerate(uris, start=1):  # Parcourt les URIs ajoutées
        sparql_query = generate_query(uri)  # Génère une requête SPARQL
        endpoint = "https://lacas.inalco.fr/portals/api/saphir/sparql_search?query="
        full_url = endpoint + requests.utils.quote(sparql_query)  # Encode l'URL de la requête
        try:
            response = requests.get(full_url)  # Envoie une requête HTTP GET
            response.raise_for_status()  # Vérifie les erreurs HTTP
            data = response.json()  # Récupère la réponse JSON
            cleaned_text, title = clean_data(data)  # Nettoie et extrait les données pertinentes
            # Affiche les résultats dans la boîte de texte
            if title:
                result_text.insert(tk.END, f"{index}-{title} {cleaned_text}\n\n\n")
            else:
                result_text.insert(tk.END, f"{index}. {cleaned_text}\n\n\n")
        except requests.RequestException as e:  # Gère les erreurs de requête
            messagebox.showerror("Erreur", f"Échec de récupération des données pour l'URI {uri}: {str(e)}")

# Fonction pour générer une requête SPARQL
def generate_query(uri):
    return f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT ?property ?content WHERE {{
      {{
        <{uri}> rdfs:label ?content .
        FILTER(LANG(?content) = "fr")
        BIND(rdfs:label AS ?property)
      }}
      UNION
      {{
        <{uri}> <http://www.ina.fr/core#fulltextSearchLabel> ?content .
        FILTER(LANG(?content) = "fr")
        BIND(<http://www.ina.fr/core#fulltextSearchLabel> AS ?property)
      }}
      UNION
      {{
        <{uri}> <http://campus-aar.fr/asa#description> ?content .
        FILTER(LANG(?content) = "fr")
        BIND(<http://campus-aar.fr/asa#description> AS ?property)
      }}
    }}
    """

# Fonction pour nettoyer et formater les données obtenues
def clean_data(data):
    title = ""  # Titre extrait
    texts = []  # Liste pour stocker les textes
    for item in data['results']['bindings']:
        # Si l'élément est un titre
        if item['property']['value'] == "http://www.w3.org/2000/01/rdf-schema#label":
            title = f"<<{item['content']['value']}>>"
        else:
            texts.append(item['content']['value'])  # Ajoute le contenu au texte global
    
    combined_text = " ".join(texts)  # Combine les textes
    filtered_text = filter_unwanted_data(combined_text)  # Filtre les données inutiles
    return filtered_text, title

# Fonction pour supprimer les données non souhaitées dans le texte
def filter_unwanted_data(text):
    # Supprime certaines données spécifiques en utilisant des expressions régulières
    text = re.sub(r';?\s*Wikimedia category \(@Wikidata\)\s*;?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(\w+:?)\s*\(@Wikidata\)\s*;?', '', text, flags=re.IGNORECASE)
    return text

# Fonction pour copier les résultats dans le presse-papier
def copy_to_clipboard():
    root.clipboard_clear()  # Efface le presse-papier
    root.clipboard_append(result_text.get("1.0", tk.END))  # Ajoute le texte au presse-papier

# Fonction pour sauvegarder les résultats dans un fichier texte
def save_as_txt():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Enregistrer sous", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:  # Ouvre un fichier pour écrire
            file.write(result_text.get("1.0", tk.END))  # Écrit les résultats dans le fichier

# Fonction pour réinitialiser l'application
def reset_all():
    uris.clear()  # Vide la liste des URIs
    logbox.delete('1.0', tk.END)  # Efface la boîte de log
    result_text.delete('1.0', tk.END)  # Efface les résultats
    logbox.insert(tk.END, "Le programme a été réinitialisé.\n")  # Message de confirmation

# Configuration de l'interface utilisateur
root = tk.Tk()
root.title("LaCAS Chapelier")

title_font = font.Font(family='Helvetica', size=24, weight='bold')  # Police du titre

# Création des éléments de l'interface
title_label = tk.Label(root, text="LaCAS Chapelier", font=title_font)
title_label.pack()

uris = []  # Liste pour stocker les URIs
tk.Label(root, text="Entrez l'URI :").pack()
uri_entry = tk.Entry(root, width=50)  # Champ de saisie
uri_entry.pack()
add_button = tk.Button(root, text="Ajouter l'URI", command=add_uri)  # Bouton pour ajouter une URI
add_button.pack()
logbox = scrolledtext.ScrolledText(root, width=60, height=5)  # Zone de log
logbox.pack(fill=tk.BOTH, expand=True)
result_text = scrolledtext.ScrolledText(root, width=60, height=10)  # Zone pour afficher les résultats
result_text.pack(fill=tk.BOTH, expand=True)
query_button = tk.Button(root, text="Exécuter les requêtes", command=run_sparql_query)  # Bouton pour exécuter les requêtes
query_button.pack()
copy_button = tk.Button(root, text="Copier dans le presse-papier", command=copy_to_clipboard)  # Bouton pour copier
copy_button.pack()
save_button = tk.Button(root, text="Enregistrer en TXT", command=save_as_txt)  # Bouton pour sauvegarder
save_button.pack()
reset_button = tk.Button(root, text="Réinitialiser", command=reset_all)  # Bouton pour réinitialiser
reset_button.pack()

# Lancement de la boucle principale
root.mainloop()

