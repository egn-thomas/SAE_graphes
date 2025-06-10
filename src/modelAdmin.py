import os
from graphe import Graphe
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

        self.graphe = None
        self.initialiser_graphe()

    def initialiser_graphe(self):
        """Initialise le graphe du magasin"""
        self.graphe = Graphe(self.nb_lignes, self.nb_colonnes)
        return self.graphe

    def get_articles_cellule(self, ligne, colonne):
        """Récupère les articles d'une cellule"""
        if (ligne, colonne) in self.articles_par_cellule:
            return self.articles_par_cellule[(ligne, colonne)]
        return []

    def ajouter_article(self, ligne, colonne, article):
        """Ajoute un article dans une cellule"""
        if (ligne, colonne) not in self.articles_par_cellule:
            self.articles_par_cellule[(ligne, colonne)] = []
        if article not in self.articles_par_cellule[(ligne, colonne)]:
            self.articles_par_cellule[(ligne, colonne)].append(article)
        
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




    




