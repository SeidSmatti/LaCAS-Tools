# LaCAS Tools

## Résumé
LaCAS Tools est un ensemble d'outils développés pour faciliter la gestion, le traitement et la publication de données au sein de l'écosystème [LaCAS](https://lacas.inalco.fr/). Ces outils couvrent une large gamme de fonctionnalités, allant de la rédaction assistée par IA à la transcription de données audio, en passant par la correction de métadonnées et l'intégration dans des vidéos. Ils sont conçus pour être accessibles, performants et respectueux de la confidentialité des utilisateurs.

## Outils

### Chapelier
Chapelier est un outil interne, développé en Python, conçu pour faciliter la rédaction de "chapôs" destinés à [LaCAS Publications](https://lacas.inalco.fr/). Il extrait et nettoie des données provenant de multiples entités de [LaCAS Data](https://lacas.inalco.fr/portals/html/resource_339623745/resource_339623745.html?portalURL=https:%2F%2Flacas.inalco.fr&portalTitle=LaCAS%20Publications). Ces données, une fois traitées, sont utilisées comme source par un LLM (Large Language Model) pour générer des textes dans un format prédéfini.

### Clean/Trans
Clean/Trans est un outil écrit en JavaScript qui facilite la correction et, éventuellement, la traduction de transcriptions réalisées avec les modèles [Whisper](https://openai.com/index/whisper/) d'OpenAI. Il nettoie le texte des métadonnées et présente une version brute, modifiable par l'utilisateur, avant de réappliquer les métadonnées au texte révisé.

### SimpleWhisper
SimpleWhisper est un outil Python qui simplifie l'utilisation des modèles Whisper grâce à une interface utilisateur intuitive. L'utilisateur peut importer un fichier audio à transcrire via des boutons dédiés. L'outil offre une solution de transcription locale, permettant de préserver la confidentialité des données tout en évitant le besoin de connaissances techniques approfondies.

### SimpleAutosubs
SimpleAutosubs est une version expérimentale de SimpleWhisper qui permet d'intégrer directement les transcriptions dans une vidéo. L'utilisateur peut charger une vidéo, sélectionner un modèle dans une liste déroulante, puis exporter la vidéo sous-titrée après traitement.

### LaCASparql
LaCASparql est un outil en JavaScript conçu pour générer des requêtes ciblant les entités LaCAS Data via une interface graphique intuitive.

### Linksfixer
Linksfixer est un outil JavaScript qui corrige certains bugs liés à la génération des URI issues de LaCAS Data, facilitant leur intégration dans LaCAS Publications.

## Licence

Ce projet est distribué sous la licence GNU GPL v3. Pour plus d'informations, consultez [ce lien](https://www.gnu.org/licenses/gpl-3.0.fr.html).

