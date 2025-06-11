import os
from graphe import Graphe
import listeProduit as lp


class MagasinModel:
    """Gère les données du magasin"""
    def __init__(self):
        # Informations de base
        self.nom_magasin = ""
        self.nom_auteur = ""
        self.nb_colonnes = 35
        self.nb_lignes = 52

        # Structure de données
        self.graphe = None
        self.categories = []
        self.produits_par_categorie = {}
        self.liste_produits = []

        self.initialiser_graphe()

    def initialiser_graphe(self):
        """Initialise le graphe du magasin"""
        self.graphe = Graphe(self.nb_lignes, self.nb_colonnes)

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




    




