import os
import cv2
import numpy as np
from graphe import Graphe
import listeProduit as lp


class MagasinModel:
    """Gère les données du magasin"""
    def __init__(self):
        self.nom_magasin = ""
        self.nom_auteur = ""
        self.seuil_blanc = 180
        self.nb_colonnes = 35
        self.nb_lignes = 56
        self.cases_rayon = self.analyser_image()

        self.graphe = None
        self.categories = []
        self.produits_par_categorie = {}
        self.liste_produits = []

        self.parent = None
        self.initialiser_graphe()

    def initialiser_graphe(self):
        """Initialise le graphe du magasin"""
        self.graphe = Graphe(self.nb_lignes, self.nb_colonnes, self.cases_rayon, self.parent)
        return self.graphe

    def ajouter_article(self, ligne, colonne, article):
        """Ajoute un article dans une cellule"""
        return self.graphe.ajouter_contenu(ligne, colonne, article)

    def get_articles_cellule(self, ligne, colonne):
        """Récupère les articles d'une cellule"""
        cellule = self.graphe.get_cellule(ligne, colonne)
        return cellule.contenu if cellule else []

    def charger_produits(self, csv_path=None):
        """Charge les produits depuis le CSV"""
        if csv_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, "..", "liste_produits.csv")
        
        try:
            self._charger_et_organiser_produits(csv_path)
            return True
        except FileNotFoundError as e:
            print(f"Erreur : fichier non trouvé à {csv_path} -> {e}")
            return False

    def _charger_et_organiser_produits(self, csv_path):
        """Charge et organise les produits par catégorie"""
        loader = lp.csvLoader(csv_path)
        produits = loader.extract_all()
        
        self.categories = produits[0]
        self.liste_produits = [dict(zip(self.categories, row)) for row in produits[1:]]
        self.produits_par_categorie = {cat: [] for cat in self.categories}
        
        for produit in self.liste_produits:
            for cat in self.categories:
                valeur = produit[cat]
                if valeur:
                    self.produits_par_categorie[cat].append(valeur)


    def analyser_image(self):
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

            largeur_case = largeur // self.nb_colonnes
            hauteur_case = hauteur // self.nb_lignes

            # Première passe : remplit viz_image avec les couleurs moyennes
            for ligne in range(self.nb_lignes):
                for colonne in range(self.nb_colonnes):
                    x_debut = colonne * largeur_case
                    y_debut = ligne * hauteur_case
                    x_fin = min(x_debut + largeur_case, largeur)
                    y_fin = min(y_debut + hauteur_case, hauteur)

                    zone = image_rgb[y_debut:y_fin, x_debut:x_fin]
                    moyenne = np.mean(zone, axis=(0, 1))

                    if np.any(moyenne < self.seuil_blanc):
                        viz_image[y_debut:y_fin, x_debut:x_fin] = (0, 0, 0)

            # Deuxième passe : détecte les cases qui ont été coloriées en noir
            cases_colorees = []
            for ligne in range(self.nb_lignes):
                for colonne in range(self.nb_colonnes):
                    x_debut = colonne * largeur_case
                    y_debut = ligne * hauteur_case
                    x_fin = min(x_debut + largeur_case, largeur)
                    y_fin = min(y_debut + hauteur_case, hauteur)

                    zone = viz_image[y_debut:y_fin, x_debut:x_fin]

                    # Vérifie si la zone est entièrement noire (0, 0, 0)
                    if np.all(zone == 0):
                        cases_colorees.append((ligne, colonne))

            # Sauvegarde de l’image de visualisation
            chemin_viz = os.path.join(script_dir, "..", "visualization.jpg")
            cv2.imwrite(chemin_viz, cv2.cvtColor(viz_image, cv2.COLOR_RGB2BGR))
            print(f"Nombre final de cases colorées (non blanches pures) : {len(cases_colorees)}")

            return cases_colorees

        except Exception as e:
            print(f"Erreur lors de l'analyse de l'image: {e}")
            return []