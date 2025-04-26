# Dépôt – Scripts de traitement cinématique et EMG

## Description
Ce dépôt rassemble les principaux scripts développés pour traiter des données de **cinématique articulaire** et d'**électromyographie (EMG)** issues de fichiers C3D.  
Il centralise les fonctions et scripts nécessaires pour extraire, corriger et analyser les signaux de mouvement et d’activité musculaire.

---

## Contenu du dépôt

### 1) Script principal
- **COMP_6_ANGLES**  
  Script principal pour l'obtention des **valeurs** et des **graphiques** des **angles articulaires** (six articulations principales) à partir des données cinématiques.  
  Ce script peut être enrichi pour intégrer les analyses synchronisées avec les signaux EMG.

### 2) Sous-branche utils
- **utils**  
  Contient un ensemble de **fonctions utilitaires** pour le traitement des fichiers C3D, notamment :
  - **Filtrage** des trajectoires et des signaux,
  - **Reconstruction** des trajectoires manquantes,
  - **Extraction et traitement des signaux EMG** (ex. filtrage passe-bande, rectification, RMS),
  - Préparation des données pour analyses conjointes cinématique/EMG.

---

## Objectifs
- **Cinématique** : extraire et analyser les **angles articulaires** huméro-thoraciques, scapulo-thoraciques, gléno-huméraux, etc.
- **EMG** : prétraiter les signaux d’activité musculaire pour une analyse fiable et exploitable.
- Proposer une **pipeline de traitement intégrée** pour synchroniser et analyser les données mouvement et EMG ensemble.

---

