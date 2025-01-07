# LaCAS Chapelier

LaCAS Chapelier est une interface graphique (GUI) développée en Python qui facilite l'exécution de requêtes SPARQL sur des URIs spécifiques. Ce programme permet de récupérer des métadonnées descriptives en français à partir de la plateforme [LaCAS](https://lacas.inalco.fr/) et de les afficher dans une interface accessible.

## Fonctionnalités

- Ajouter des URIs pour exécuter des requêtes SPARQL.
- Générer des requêtes SPARQL pour obtenir des propriétés et des contenus liés à une entité via son URI.
- Nettoyer et structurer les données récupérées.
- Afficher les résultats dans une interface graphique intuitive.
- Copier les résultats dans le presse-papier.
- Enregistrer les résultats dans un fichier texte.
- Réinitialiser l'application pour un nouvel usage.

## Prérequis

Avant d'utiliser LaCAS Chapelier, assurez-vous que les éléments suivants sont installés :

- Python 3.x
- Les bibliothèques Python suivantes :
  - `tkinter` (inclus par défaut avec Python sur la plupart des systèmes)
  - `requests`
  - `re`

## Installation

1. Clonez le dépôt GitHub contenant l'ensemble des outils LaCAS :
   ```bash
   git clone https://github.com/SeidSmatti/LaCAS-Tools.git
   cd LaCAS-Tools/Chapelier
   ```

2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Lancez le programme en exécutant le script Python :
   ```bash
   python Chapelier.py
   ```

2. Entrez l'URI dans le champ prévu et cliquez sur "Ajouter l'URI".

3. Appuyez sur "Exécuter les requêtes" pour lancer les requêtes SPARQL.

4. Consultez les résultats dans la section prévue. Vous pouvez également :
   - Copier les résultats dans le presse-papier en cliquant sur "Copier dans le presse-papier".
   - Enregistrer les résultats sous forme de fichier texte en cliquant sur "Enregistrer en TXT".
   - Réinitialiser l'application pour effacer les URIs et les résultats.

## Licence

Ce projet est sous licence [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html). Vous êtes libre de l'utiliser, de le modifier et de le redistribuer dans le respect des termes de cette licence.

