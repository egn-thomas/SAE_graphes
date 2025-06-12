# SAE_graphes

Dépôt GitHub pour le projet SAE Graphes  
Auteurs :
- Eugène Thomas  
- Fremy Lara  
- Kerckhove Célien  
- Doffagne Timéo

## Application de GPS appliquée à un magasin

Cette application a pour objectif principal de permettre à un utilisateur d'optimiser ses déplacements lors de son parcours dans un magasin.

Une interface Admin permet la gestion du magasin, le paramétrage de la disposition des rayons, et l'enregistrement de l'état du plan.

## Fonctionnalités

### Remplissage du magasin

- Une liste de tous les articles disponibles est affichée à gauche de l’écran.
- Il est possible de naviguer entre les catégories d’articles ou d’utiliser la barre de recherche pour filtrer les résultats.
- Un système de glisser-déposer permet de placer les produits directement sur le plan du magasin.
- Un champ de texte permet d’enregistrer le nom du magasin.

### Gestion du magasin

Les boutons de contrôle sont situés en bas à gauche :
- **Ouvrir** : charger un fichier CSV représentant un magasin.
- **Sauvegarder** : enregistre la disposition actuelle dans un fichier CSV.
- **Effacer** : réinitialise la disposition actuelle du magasin.

Une bibliothèque de magasins pré-enregistrés est déjà présente dans `magasins/`

Une sauvegarde automatique est effectuée en continu dans un fichier `sauvegarde_rapide.csv` pour prévenir les pertes de données.

La grille du magasin est ajustable via des boîtes numériques.

### Interactions avancées

- Un clic sur une case du magasin affiche un popup avec les articles qu'elle contient.
- Il est possible de supprimer un article de la case en cliquant sur son nom dans le popup.

## Langages et technologies utilisés

- Python 3
- PyQt6
- Fichiers CSV pour la persistance des données

## Organisation du projet

```bash
sae_graphe/
├── src/
│   ├── main.py
│   ├── vueAdmin.py
│   ├── controllerAdmin.py
│   ├── droparea.py
│   ├── graphe.py
│   └── (...)
├── magazins/
│   ├── magasin1.csv
│   ├── magasin2.csv
│   └── (...)
├── disposition_magasin_sauvegardee.csv
├── sauvegarde_rapide.csv
├── plan_magazin.jpg
├── liste_produits.csv
└── README.md
