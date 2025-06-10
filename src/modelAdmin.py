import os
import listeProduit as lp


class MagasinModel:
    """Modèle gérant les données du magasin et les produits"""
    
    def __init__(self):
        self.nom_magasin = ""
        self.nom_auteur = ""

        self.nb_colonnes = 35
        self.nb_lignes = 52

        self.articles_par_cellule = {}

        self.produits_par_categorie = {}
        self.categories = []
        self.liste_produits = []
    
    def ajouter_article(self, ligne, colonne, article):
        """Ajoute un article dans une cellule"""
        cellule = (ligne, colonne)
        if cellule not in self.articles_par_cellule:
            self.articles_par_cellule[cellule] = []
        if article not in self.articles_par_cellule[cellule]:
            self.articles_par_cellule[cellule].append(article)
    
    def get_articles_cellule(self, ligne, colonne):
        """Récupère les articles d'une cellule"""
        return self.articles_par_cellule.get((ligne, colonne), [])
        
    def charger_produits(self, csv_path=None):
        """Charge les produits depuis le fichier CSV"""
        if csv_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, "..", "liste_produits.csv")
        
        try:
            loader = lp.csvLoader(csv_path)
            produits = loader.extract_all()
            
            self.categories = produits[0]
            self.liste_produits = [dict(zip(self.categories, row)) for row in produits[1:]]
            
            # Organiser les produits par catégorie
            self.produits_par_categorie = {cat: [] for cat in self.categories}
            
            for produit in self.liste_produits:
                for cat in self.categories:
                    valeur = produit[cat]
                    if valeur:
                        self.produits_par_categorie[cat].append(valeur)
                        
            return True
            
        except FileNotFoundError as e:
            print(f"Erreur : fichier non trouvé à {csv_path} -> {e}")
            return False
    
    def get_categories(self):
        """Retourne la liste des catégories"""
        # todo
    
    def get_produits_par_categorie(self, categorie):
        """Retourne les produits d'une catégorie donnée"""
        # todo
             
    def set_nom_magasin(self, nom):
        """Définit le nom du magasin"""
        # todo
    
    def get_nom_magasin(self):
        """Retourne le nom du magasin"""
        # todo

    
    def set_dimensions_grille(self, colonnes, lignes):
        """Définit les dimensions de la grille"""
        # todo
        
    
    def get_dimensions_grille(self):
        """Retourne les dimensions de la grille (colonnes, lignes)"""
        # todo
        
    
    def placer_produit(self, ligne, colonne, produit):
        """Place un produit à une position donnée dans la grille"""
        # todo

    
    def retirer_produit(self, ligne, colonne):
        """Retire un produit d'une position donnée"""
        # todo

    
    def get_produit_a_position(self, ligne, colonne):
        """Retourne le produit à une position donnée"""
        # todo


class Cellule:
    """Les cellules du magazin"""
    def __init__(self, ligne, colonne, rayon=False):
        self.ligne = ligne
        self.colonne = colonne
        self.rayon = rayon
        self.articles = []
        self.voisins = []

    def ajouter_voisin(self, cellule):
        """Ajoute un voisin"""
    
    def est_accessible(self, autre_cellule):
        """Vérifie si deux cellules sont accessibles entre elles"""
        return (autre_cellule in self.voisins and 
                (not self.est_rayon or not autre_cellule.est_rayon))

class Graphe:
    """Le graphe représentatif du magazin"""
    def __init__(self, nb_lignes, nb_colonnes):
        self.nb_lignes = nb_lignes
        self



