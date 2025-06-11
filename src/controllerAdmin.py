from PyQt6.QtCore import QObject
from modelAdmin import MagasinModel
from vueAdmin import VueAdmin
from cellule import Cellule
from graphe import Graphe


class MagasinController(QObject):
    """Contrôleur gérant la logique entre le modèle et la vue"""
    
    def __init__(self):
        super().__init__()
        self.model = MagasinModel()
        self.vue = VueAdmin()
        self.connecter_signaux()
        self.initialiser()
    
    def connecter_signaux(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur"""
        # Signaux principaux de la vue
        self.vue.categorie_cliquee.connect(self.afficher_produits_categorie)
        self.vue.retour_categories.connect(self.afficher_categories)
        self.vue.placer_produit.connect(self.placer_produit)
        self.vue.cellule_cliquee.connect(self.cellule_cliquee)

    def initialiser(self):
        """Initialise l'application avec les données de base"""
        if self.model.charger_produits():
            self.afficher_categories()
        else:
            print("Erreur lors du chargement des produits")

    def cellule_cliquee(self, ligne, colonne):
        """Gère le clic sur une cellule"""
        articles = self.model.get_articles_cellule(ligne, colonne)
        self.vue.afficher_popup_articles(ligne, colonne, articles)

    def placer_produit(self, ligne, colonne, produit):
        """Place un produit dans la grille"""
        if self.model.ajouter_article(ligne, colonne, produit):
            print(f"[DEBUG] Produit '{produit}' placé en ({ligne}, {colonne})")
        else:
            print(f"[DEBUG] Échec du placement de '{produit}' en ({ligne}, {colonne})")
    
    
    def afficher_categories(self):
        """Affiche la liste des catégories dans la vue"""
        categories = self.model.produits_par_categorie.keys()
        self.vue.afficher_categories(categories)

    def afficher_produits_categorie(self, categorie):
        """Affiche les produits d'une catégorie donnée"""
        print(f"[DEBUG] Categorie cliquée : {categorie}")
        produits = self.model.produits_par_categorie.get(categorie, [])
        self.vue.afficher_produits(produits)