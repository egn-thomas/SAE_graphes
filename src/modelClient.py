import os
import cv2
import csv
import numpy as np
from graphe import Graphe
import listeProduit as lp
from listeProduit import CsvLoader


class ClientModel:
    """Gère les données du magasin"""
    def __init__(self):
        self.nom_magasin = ""
        self.nom_auteur = ""
        self.seuil_blanc = 180
        self.nb_colonnes = 35
        self.nb_lignes = 56
        self.cases_rayon = self.analyser_image(self.nb_colonnes, self.nb_lignes)

        self.graphe = None
        self.categories = []
        self.produits_par_categorie = {}
        self.liste_produits = []
        self.liste_panier = []

        self.parent = None
        self.initialiser_graphe()

    def initialiser_graphe(self):
        """Initialise le graphe du magasin"""
        self.graphe = Graphe(self.nb_lignes, self.nb_colonnes, self.cases_rayon, self.parent)
        return self.graphe
    
    def ajouter_produit(self, nom_produit):
        """ajoute le produit a la liste"""
        self.liste_panier.append(nom_produit)
        print (self.liste_panier)
    
    def effacer_element_grille(self, ligne, colonne, produit):
        """Supprime un élément spécifique du CSV en fonction de la ligne, colonne et produit."""
        print(f"[MODÈLE] Suppression de {produit} à ({ligne}, {colonne})")
        lignes_conservees = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin = os.path.join(script_dir, "..", "magasins/sauvegarde_rapide.csv")
        with open(chemin, "r", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for lignecsv in reader:
                if lignecsv == ["Nom du projet", "Nom du produit", "X", "Y", "Position"]:
                    lignes_conservees.append(lignecsv)
                    continue
                
                if (len(lignecsv) >= 5 and 
                    lignecsv[1] == produit and 
                    lignecsv[2] == str(colonne) and 
                    lignecsv[3] == str(ligne)):
                    continue
                else:
                    lignes_conservees.append(lignecsv)
        
        with open(chemin, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(lignes_conservees)

    def ajouter_article(self, ligne, colonne, article):
        """Ajoute un article dans une cellule"""
        return self.graphe.ajouter_contenu(ligne, colonne, article)

    def get_articles_cellule(self, ligne, colonne):
        """Récupère les articles d'une cellule"""
        cellule = self.graphe.get_cellule(ligne, colonne)
        return cellule.contenu if cellule else []
    
    def charger_produits(self,  nom_fichier, nom_magasin, csv_path=None):
        """Charge les produits depuis le CSV"""
        if csv_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, "..", nom_fichier)
        try:
            self._charger_et_organiser_produits(csv_path, nom_magasin)
            return True
        except FileNotFoundError as e:
            print(f"Erreur : fichier non trouvé à {csv_path} -> {e}")
            return False

    def _charger_et_organiser_produits(self, csv_path, magasin):
        """Charge et organise les produits par catégorie"""
        loader = CsvLoader(csv_path)
        produits = loader.extraire_articles_par_categorie(magasin, "../liste_produits.csv")
        
        self.categories = produits[0]
        self.liste_produits = [dict(zip(self.categories, row)) for row in produits[1:]]
        self.produits_par_categorie = {cat: [] for cat in self.categories}
        
        for produit in self.liste_produits:
            for cat in self.categories:
                valeur = produit[cat]
                if valeur:
                    self.produits_par_categorie[cat].append(valeur)


    def analyser_image(self, rows, cols):
        """Analyse l'image du plan pour détecter les rayons selon la couleur moyenne"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin_image = os.path.join(script_dir, "..", "plan_magasin.jpg")
        
        try:
            image = cv2.imread(chemin_image)
            if image is None:
                print("Erreur : Impossible de charger l'image.")
                return []

            # Conversion et rotation
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb = cv2.rotate(image_rgb, cv2.ROTATE_90_CLOCKWISE)
            hauteur, largeur = image_rgb.shape[:2]

            # Image de visualisation : blanc par défaut
            viz_image = np.full((hauteur, largeur, 3), 255, dtype=np.uint8)

            largeur_case = largeur // cols
            hauteur_case = hauteur // rows

            # Première passe : remplit viz_image avec les couleurs moyennes
            for ligne in range(rows):
                for colonne in range(cols):
                    x_debut = colonne * largeur_case
                    y_debut = ligne * hauteur_case
                    x_fin = min(x_debut + largeur_case, largeur)
                    y_fin = min(y_debut + hauteur_case, hauteur)

                    zone = image_rgb[y_debut:y_fin, x_debut:x_fin]
                    moyenne = np.mean(zone, axis=(0, 1))

                    if np.any(moyenne < self.seuil_blanc):
                        viz_image[y_debut:y_fin, x_debut:x_fin] = (0, 0, 0)

            # Deuxième passe : détecte les cases noires
            cases_colorees = []
            for ligne in range(rows):
                for colonne in range(cols):
                    x_debut = colonne * largeur_case
                    y_debut = ligne * hauteur_case
                    x_fin = min(x_debut + largeur_case, largeur)
                    y_fin = min(y_debut + hauteur_case, hauteur)

                    zone = viz_image[y_debut:y_fin, x_debut:x_fin]
                    if np.all(zone == 0):
                        cases_colorees.append((ligne, colonne))

            return cases_colorees

        except Exception as e:
            print(f"Erreur lors de l'analyse de l'image: {e}")
            return []