from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from modelAdmin import MagasinModel
from vueAdmin import VueAdmin
from login import PageConnexion


class MagasinController(QObject):
    """Contrôleur gérant la logique entre le modèle et la vue"""
    
    def __init__(self):
        super().__init__()
        self.vue = VueAdmin()
        self.model = MagasinModel()
        self.model.parent = self.vue
        self.categorie_courante = None
        self.retour_connexion = False
        self.connecter_signaux()
        self.initialiser()
        
        self.timer_colonnes_spinbox = QtCore.QTimer()
        self.timer_colonnes_spinbox.setSingleShot(True)
        self.timer_colonnes_spinbox.timeout.connect(self._appliquer_changement_colonnes)

        self.timer_lignes_spinbox = QtCore.QTimer()
        self.timer_lignes_spinbox.setSingleShot(True)
        self.timer_lignes_spinbox.timeout.connect(self._appliquer_changement_lignes)
    
    def connecter_signaux(self):
        """Connecte les signaux de la vue aux méthodes du contrôleur"""
        self.vue.bouton_effacer.clicked.connect(self.effacer_projet)
        self.vue.nom_magasin.textChanged.connect(self.mise_a_jour_nom_magasin)
        self.vue.recherche_articles.textChanged.connect(self.filtrer_produits)
        self.vue.categorie_cliquee.connect(self.afficher_produits_categorie)
        self.vue.retour_categories.connect(self.afficher_categories)
        self.vue.placer_produit.connect(self.placer_produit)
        self.vue.cellule_cliquee.connect(self.cellule_cliquee)
        self.vue.recherche_changee.connect(self.filtrer_produits)
        self.vue.spinTableauBordColonnes.valueChanged.connect(self.timer_colonnes)
        self.vue.spinTableauBordLignes.valueChanged.connect(self.timer_lignes)
        self.vue.bouton_popup_signal.connect(self.supprimer_article)
        self.vue.deconnexion_signal.connect(self.deconnecter)

    def initialiser(self):
        """Initialise l'application avec les données de base"""
        if self.model.charger_produits():
            self.afficher_categories()
        else:
            print("Erreur lors du chargement des produits")

    def supprimer_article(self, ligne, colonne, produit):
        print(f"[CONTROLLER] Suppression de {produit} à ({ligne}, {colonne}) demandée")
        self.model.effacer_element_grille(ligne, colonne, produit)
        self.vue.supprimer_article_cellule(ligne, colonne, produit)

    def deconnecter(self):
        print("[DEBUG] : deconnexion demandée")
        self.retour_connexion = True
        self.vue.close()
    
    def timer_colonnes(self):
        self.timer_colonnes_spinbox.start(1000)
    
    def _appliquer_changement_colonnes(self):
        valeur = self.vue.spinTableauBordColonnes.value()
        self.changer_colonnes(valeur)

    def changer_colonnes(self, valeur):
        print(f"Colonnes modifiées : {valeur}")
        self.model.nb_colonnes = valeur
        self.vue.mettre_a_jour_grille(self.model.nb_colonnes, valeur)
        self.model.initialiser_graphe()

    def timer_lignes(self):
        self.timer_lignes_spinbox.start(1000)
    
    def _appliquer_changement_lignes(self):
        valeur = self.vue.spinTableauBordLignes.value()
        self.changer_lignes(valeur)

    def changer_lignes(self, valeur):
        print(f"Lignes modifiées : {valeur}")
        self.model.nb_lignes = valeur
        self.vue.mettre_a_jour_grille(valeur, self.model.nb_colonnes)
        self.model.initialiser_graphe()

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