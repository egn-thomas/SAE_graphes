import os
import cv2
import numpy as np
from graphe import Graphe
import listeProduit as lp


class MagasinModel:
    """Gère les données du magasin"""
    def __init__(self):
        # Informations de base
        self.nom_magasin = ""
        self.nom_auteur = ""
        self.nb_colonnes = 56
        self.nb_lignes = 35
        self.cases_rayon = self.analyser_image()

        # Structure de données
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

    def calculer_pourcentage_blanc(self, case):
        """
        Calcule le pourcentage de pixels blancs dans une case
        """
        seuil_pixel_blanc = 100
        
        pixels_blancs = np.sum(np.all(case >= seuil_pixel_blanc, axis=2))
        pixels_totaux = case.shape[0] * case.shape[1]
        
        if pixels_totaux == 0:
            return 0
        
        pourcentage = (pixels_blancs / pixels_totaux) * 100

        return pourcentage

    
    def analyser_image(self):
        
        chemin_image = "plan_magasin.png"  
        
        try:
            image = cv2.imread(chemin_image)
            if image is None:
                print("Erreur : Impossible de charger l'image. Vérifiez le chemin.")
                return

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            hauteur, largeur = image_rgb.shape[:2]
            
            print(f"Image chargée : {largeur}x{hauteur} pixels")
            
            nb_colonnes = 56
            nb_lignes = 35
            seuil_blanc = 80
            
            largeur_case = largeur // nb_colonnes
            hauteur_case = hauteur // nb_lignes
            
            print(f"Taille de chaque case : {largeur_case}x{hauteur_case} pixels")
            
            cases_colorees = []

            for ligne in range(nb_lignes):
                for colonne in range(nb_colonnes):
                    x_debut = colonne * largeur_case
                    y_debut = ligne * hauteur_case
                    x_fin = min(x_debut + largeur_case, largeur)
                    y_fin = min(y_debut + hauteur_case, hauteur)
                    
                    case = image_rgb[y_debut:y_fin, x_debut:x_fin]

                    pourcentage_blanc = self.calculer_pourcentage_blanc(case)

                    if pourcentage_blanc < seuil_blanc:
                        cases_colorees.append((colonne, ligne))
                        print(f"Case colorée trouvée : ({colonne},{ligne}) - {pourcentage_blanc:.1f}% de blanc")
                    else:
                        print(f"Case blanche skippée : ({colonne},{ligne}) - {pourcentage_blanc:.1f}% de blanc")

            print(f"\n=== RÉSULTATS ===")
            print(f"Nombre total de cases : {nb_colonnes * nb_lignes}")
            print(f"Nombre de cases colorées : {len(cases_colorees)}")
            print(f"Nombre de cases blanches (skippées) : {nb_colonnes * nb_lignes - len(cases_colorees)}")
            
            print(f"\nCoordonnées des cases colorées :")
            for coord in cases_colorees:
                print(f"  {coord}")
            
            return cases_colorees
            
        except Exception as e:
            print(f"Erreur : {e}")
            return None
