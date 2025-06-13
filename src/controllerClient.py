from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from modelClient import ClientModel
from vueClient import VueClient
from graphe import Graphe
from login import PageConnexion


class ClientController(QObject):
    """Contrôleur gérant la logique entre le modèle et la vue"""
    
    def __init__(self):
        super().__init__()
        self.vue = VueClient()
        self.model = ClientModel()
        self.graphe = Graphe(35, 52, self.model.cases_rayon)
        self.articles = {}
        self.chemin_rapide = []
        self.model.parent = self.vue
        self.categorie_courante = None
        self.retour_connexion = False
        self.connecter_signaux()
        self.initialiser()
    
    def connecter_signaux(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur"""
        self.vue.nom_magasin.textChanged.connect(self.mise_a_jour_nom_magasin)
        self.vue.recherche_articles.textChanged.connect(self.filtrer_produits)
        self.vue.categorie_cliquee.connect(self.afficher_produits_categorie)
        self.vue.retour_categories.connect(self.afficher_categories)
        self.vue.recherche_changee.connect(self.filtrer_produits)
        self.vue.deconnexion_signal.connect(self.deconnecter)
        self.vue.ouvrir_signal.connect(self.ouvrir_magasin)
        self.vue.enlever_produit_signal.connect(self.enlever_du_panier)
        self.vue.produit_signal.connect(self.ajouter_au_panier)
        self.vue.effacer_signal.connect(self.enlever_tout_panier)

    def initialiser(self):
        """Initialise l'application avec les données de base"""

    def enlever_tout_panier(self):
        """vide le liste en le layout panier"""
        self.vue.clear_layout(self.vue.layout_panier)
        self.model.clear_panier()

    def ajouter_au_panier(self, nom_produit):
        """ajoute le produit correspondant au panier et recalcule le chemin"""
        self.vue.ajouter_produit(nom_produit)
        self.model.ajouter_produit(nom_produit)
        self.chemin_rapide = self.graphe.generer_chemin_complet(self.model.liste_panier, position_depart=(4,38))
        print (self.chemin_rapide)
        for (i, j) in self.chemin_rapide:
            self.vue.colorier_cellule_en_orange(i, j)

    def enlever_du_panier(self, nom_produit):
        """enlève un produit du panier"""
        self.vue.enlever_produit(nom_produit)
        self.model.enlever_produit(nom_produit)

    def ouvrir_magasin(self, fichier):
        """ouvre un magazin pour remplir la liste"""
        if self.model.charger_produits("liste_produits.csv", fichier):
            self.vue.afficher_categories(self.model.produits_par_categorie.keys())
            self.articles = self.graphe.charger_catalogue_depuis_csv(fichier)
        else:
            print(f"Échec du chargement du fichier : {fichier}")

    def supprimer_article(self, ligne, colonne, produit):
        print(f"[CONTROLLER] Suppression de {produit} à ({ligne}, {colonne}) demandée")
        self.model.effacer_element_grille(ligne, colonne, produit)
        self.vue.supprimer_article_cellule(ligne, colonne, produit)

    def deconnecter(self):
        print("[DEBUG] : deconnexion demandée")
        self.retour_connexion = True
        self.vue.close()

    def changer_colonnes(self, valeur):
        print(f"Colonnes modifiées : {valeur}")
        self.model.nb_colonnes = valeur
        self.vue.mettre_a_jour_grille(self.model.nb_lignes, valeur)
        self.model.initialiser_graphe()

    def changer_lignes(self, valeur):
        print(f"Lignes modifiées : {valeur}")
        self.model.nb_lignes = valeur
        self.vue.mettre_a_jour_grille(valeur, self.model.nb_colonnes)
        self.model.initialiser_graphe()

    def timer_lignes(self):
        valeur_initiale = self.vue.spinTableauBordLignes.value()

        def verifier_stabilite():
            valeur_actuelle = self.vue.spinTableauBordLignes.value()
            if valeur_actuelle == valeur_initiale:
                self.changer_lignes(valeur_actuelle)

        QtCore.QTimer.singleShot(1000, verifier_stabilite)

    def filtrer_produits(self, texte_recherche):
        """Filtre les produits selon le texte de recherche dans toutes les catégories"""
        if not texte_recherche:  # Si la recherche est vide, afficher la catégorie courante
            if self.categorie_courante:
                produits = self.model.produits_par_categorie.get(self.categorie_courante, [])
                self.vue.afficher_produits(produits)
            return

        produits_filtres = []
        for categorie, produits in self.model.produits_par_categorie.items():
            for produit in produits:
                if texte_recherche.lower() in produit.lower():
                    produits_filtres.append(produit)
        
        self.vue.afficher_produits(produits_filtres)

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
        self.categorie_courante = categorie
        produits = self.model.produits_par_categorie.get(categorie, [])
        texte_recherche = self.vue.recherche_articles.text()
        if texte_recherche:
            produits = [p for p in produits if texte_recherche.lower() in p.lower()]
        self.vue.afficher_produits(produits)
        print(f"[DEBUG] Affichage des produits de la catégorie : {categorie}")

    def mise_a_jour_nom_magasin(self, nouveau_nom):
        """Met à jour le nom du magasin dans le modèle et le fichier CSV"""
        self.model.nom_magasin = nouveau_nom
        self.vue.maj_nom_projet_csv(nouveau_nom)
    
    def effacer_projet(self):
        """Gère l'effacement complet du projet"""
        self.vue.effacer_projet()