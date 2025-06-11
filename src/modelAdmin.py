import os
import cv2
import numpy as np
from graphe import Graphe
import listeProduit as lp


class MagasinModel:
    """Gère les données du magasin"""
    COULEURS_RAYONS = {
        'BOUCHERIE': (255, 0, 0),     # Rouge vif
        'CHARCUTERIE': (255, 165, 0),  # Orange
        'BAZAR': (255, 215, 0),        # Jaune vif
        'TEXTILE': (0, 128, 128),      # Turquoise foncé
        'EPICERIE': (0, 100, 0),       # Vert foncé
        'SAISONNIER': (46, 139, 87),   # Vert mer
        'FRUITS': (50, 205, 50),       # Vert clair
        'ENTRETIEN': (152, 251, 152),  # Vert pâle
        'PATISSERIE': (210, 180, 140), # Beige
        'INFORMATIQUE': (0, 0, 139)    # Bleu foncé
    }
    def __init__(self):
        # Informations de base
        self.nom_magasin = ""
        self.nom_auteur = ""
        self.seuil_blanc = 254
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

    def calculer_couleur_dominante(self, case):
        """
        Calcule la couleur dominante d'une case et la mappe à la couleur de rayon la plus proche
        """
        pixels = case.reshape(-1, 3)
        pixels_tuples = [tuple(pixel) for pixel in pixels]
        from collections import Counter
        couleurs_count = Counter(pixels_tuples)
        couleur_dominante = np.array(max(couleurs_count.items(), key=lambda x: x[1])[0])
        
        # Si la case est très blanche, retourner blanc
        if np.mean(couleur_dominante) > self.seuil_blanc:
            return np.array([255, 255, 255])
        
        # Sinon, trouver la couleur de rayon la plus proche
        distances = {
            nom: np.sum(np.abs(couleur_dominante - np.array(couleur)))
            for nom, couleur in self.COULEURS_RAYONS.items()
        }
        couleur_proche = self.COULEURS_RAYONS[min(distances.items(), key=lambda x: x[1])[0]]
        return np.array(couleur_proche)

    def analyser_image(self):
        """Analyse l'image du plan pour détecter les rayons et crée une visualisation"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin_image = os.path.join(script_dir, "..", "plan_magasin.jpg")
        
        try:
            image = cv2.imread(chemin_image)
            if image is None:
                print("Erreur : Impossible de charger l'image.")
                return []

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            hauteur, largeur = image_rgb.shape[:2]
            
            # Créer une image pour la visualisation
            viz_image = np.zeros((hauteur, largeur, 3), dtype=np.uint8)
            cases_colorees = []

            for ligne in range(self.nb_lignes):
                for colonne in range(self.nb_colonnes):
                    x_debut = colonne * (largeur // self.nb_colonnes)
                    y_debut = ligne * (hauteur // self.nb_lignes)
                    x_fin = min(x_debut + (largeur // self.nb_colonnes), largeur)
                    y_fin = min(y_debut + (hauteur // self.nb_lignes), hauteur)
                    
                    case = image_rgb[y_debut:y_fin, x_debut:x_fin]
                    
                    # Calculer la couleur dominante
                    couleur_dominante = self.calculer_couleur_dominante(case)
                    
                    # Si ce n'est pas du blanc, dessiner avec des bordures noires
                    if not np.array_equal(couleur_dominante, [255, 255, 255]):
                        # Remplir l'intérieur de la case
                        viz_image[y_debut+2:y_fin-2, x_debut+2:x_fin-2] = couleur_dominante
                        # Dessiner les bordures noires
                        viz_image[y_debut:y_fin, x_debut:x_debut+2] = [0, 0, 0]  # Bordure gauche
                        viz_image[y_debut:y_fin, x_fin-2:x_fin] = [0, 0, 0]      # Bordure droite
                        viz_image[y_debut:y_debut+2, x_debut:x_fin] = [0, 0, 0]  # Bordure haute
                        viz_image[y_fin-2:y_fin, x_debut:x_fin] = [0, 0, 0]      # Bordure basse
                        cases_colorees.append((colonne, ligne))
            
            # Sauvegarder l'image de visualisation
            chemin_viz = os.path.join(script_dir, "..", "visualization.jpg")
            cv2.imwrite(chemin_viz, cv2.cvtColor(viz_image, cv2.COLOR_RGB2BGR))
            print(f"Image de visualisation sauvegardée : {chemin_viz}")

            return cases_colorees

        except Exception as e:
            print(f"Erreur lors de l'analyse de l'image: {e}")
            return []
        
    def set_seuil_blanc(self, nouvelle_valeur):
        """Change le seuil de détection du blanc"""
        self.seuil_blanc = nouvelle_valeur
        self.cases_rayon = self.analyser_image()
        self.initialiser_graphe()



    




