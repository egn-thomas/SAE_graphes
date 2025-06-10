import os
import listeProduit as lp


class MagasinModel:
    """Modèle gérant les données du magasin et les produits"""
    
    def __init__(self):
        self.nom_magasin = ""
        self.nb_colonnes = 35
        self.nb_lignes = 52
        self.produits_par_categorie = {}
        self.grille_produits = {}  # Position -> nom_produit
        self.categories = []
        self.liste_produits = []
        
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


