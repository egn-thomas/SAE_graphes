from PyQt6.QtCore import QObject
from modelAdmin import MagasinModel
from vueAdmin import VueAdmin


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
        self.vue.categorie_cliquee.connect(self.afficher_produits_categorie)
        self.vue.retour_categories.connect(self.afficher_categories)
        self.vue.dimensions_changees.connect(self.changer_dimensions_grille)
        self.vue.nom_magasin_change.connect(self.changer_nom_magasin)
        self.vue.produit_place.connect(self.placer_produit)
        for cellule in self.vue.cellules_grille.values():
            cellule.produit_place.connect(self.produit_place)
            cellule.cellule_cliquee.connect(self.cellule_cliquee)

    def produit_place(self, ligne, colonne, produit):
        """Gère le placement d'un produit"""
        self.model.ajouter_article(ligne, colonne, produit)
    
    def cellule_cliquee(self, ligne, colonne):
        """Gère le clic sur une cellule"""
        articles = self.model.get_articles_cellule(ligne, colonne)
        self.vue.afficher_popup_articles(ligne, colonne, articles)
    
    def initialiser(self):
        """Initialise l'application avec les données de base"""
        # Charger les produits depuis le CSV
        if self.model.charger_produits():
            self.afficher_categories()
        else:
            print("Erreur lors du chargement des produits")
    
    def afficher_categories(self):
        """Affiche la liste des catégories dans la vue"""
        categories = self.model.produits_par_categorie.keys()
        self.vue.afficher_categories(categories)

    def afficher_produits_categorie(self, categorie):
        """Affiche les produits d'une catégorie donnée"""
        print(f"[DEBUG] Categorie cliquée : {categorie}")
        produits = self.model.produits_par_categorie.get(categorie, [])
        self.vue.afficher_produits(produits)
    
    def changer_dimensions_grille(self, colonnes, lignes):
        """Change les dimensions de la grille"""
        # todo
    
    def changer_nom_magasin(self, nom):
        """Change le nom du magasin"""
        # todo
    
    def placer_produit(self, ligne, colonne, produit):
        """Place un produit dans la grille"""
        # todo