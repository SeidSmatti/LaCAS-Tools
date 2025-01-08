# Outils LaCAS - Links fixer

## Aperçu
Links fixer est outil interne permettant d'obtenir les URI d'entités issues de LaCAS Data afin de les intégrer à LaCAS Publications.

## Fonctionnalités

- **Sélection du Domaine de Ressource :** Les utilisateurs peuvent sélectionner des domaines spécifiques à partir d'une liste prédéfinie, incluant des données filmiques, textuelles, visuelles, sonores, et plus, pour adapter leurs requêtes de recherche à des domaines d'intérêt particuliers.
- **Génération de Requêtes pour les Entités FAIRisées :** Fournit une interface pour que les utilisateurs puissent entrer des identifiants FAIR et des étiquettes, générant des requêtes SPARQL prêtes à l'emploi qui récupèrent des informations détaillées sur l'entité FAIRisée spécifiée.
- **Génération de Requêtes pour les Entités Non-FAIRisées :** De manière similaire aux entités FAIRisées, cette fonctionnalité permet aux utilisateurs d'entrer des URI complètes et des étiquettes pour des entités non-FAIRisées, générant des requêtes SPARQL pour récupérer des données de la base de données LaCAS.
- **Conception Réactive :** Assure l'accessibilité et la facilité d'utilisation sur différents appareils grâce à une mise en page réactive qui s'adapte aux tailles d'écran.

## Utilisation

1. **Sélection d'un Domaine de Ressource :** À partir du menu déroulant, choisissez le domaine spécifique sur lequel vous souhaitez effectuer une requête.
2. **Génération de Requêtes pour les Entités FAIRisées :**
   - Entrez l'identifiant FAIR et l'étiquette pour l'entité que vous souhaitez interroger.
   - Cliquez sur le bouton "Générer la requête" pour générer la requête.
   - Utilisez le bouton "Copier dans le presse-papiers" pour copier la requête générée dans votre presse-papiers.
3. **Génération de Requêtes pour les Entités Non-FAIRisées :**
   - Entrez l'URI complète et l'étiquette pour l'entité non-FAIRisée.
   - Cliquez sur le bouton "Générer la requête" pour créer la requête.
   - Utilisez le bouton "Copier dans le presse-papiers" pour copier la requête pour utilisation.

## Détails Techniques

- **HTML/CSS :** L'outil utilise HTML pour la structure et CSS pour le style, avec une conception réactive qui s'adapte à diverses tailles d'écran.
- **JavaScript :** Les fonctionnalités principales, incluant la génération de requête et les opérations de presse-papiers, sont implémentées en JavaScript.

## Installation

Aucune installation n'est requise. L'outil est basé sur le web et peut être accédé en utilisant n'importe quel navigateur web moderne.
