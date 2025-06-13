from graphe import Graphe
from droparea import DropArea
from modelClient import ClientModel
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QFileDialog, QFrame
from collections import Counter
import os
import csv

class VueClient(QtWidgets.QWidget):
    """Vue principale de l'interface client héritant de VueGraphe"""
    
    # Signaux pour communiquer avec le contrôleur
    categorie_cliquee = QtCore.pyqtSignal(str)
    retour_categories = QtCore.pyqtSignal()
    nom_magasin_change = QtCore.pyqtSignal(str)
    recherche_changee = QtCore.pyqtSignal(str)
    deconnexion_signal = QtCore.pyqtSignal()
    ouvrir_signal = QtCore.pyqtSignal(str)
    effacer_signal = QtCore.pyqtSignal()
    produit_signal = QtCore.pyqtSignal(str)
    enlever_produit_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        """Initialise l'interface utilisateur"""
        super().__init__()  # Appelle correctement le constructeur parent
        
        self.setWindowTitle("Parcours d'un magasin")
        self.setGeometry(200, 200, 1600, 1200)
        
        # Variables d'instance
        self.position_actuelle = (37, 3)
        self.liste_courses = []
        
        # Création de l'interface
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Créer les composants de l'interface
        self.create_partie_gauche()
        self.create_partie_droite()
        
        # Connexions des signaux
        self.sauvegarder_signal.connect(self.sauvegarder_tous_les_produits)
        self.connecter_signaux()
        self.initialiser_sauvegarde()
        self.popup_actuelle = None

        # Marquer l'entrée une fois que tout est initialisé
        if self.graphe and self.position_actuelle in self.graphe.cellules_graphiques:
            self.graphe.cellules_graphiques[self.position_actuelle].marquer_comme_entree()
    
    
    def initialiser_sauvegarde(self):
        """Crée un fichier de sauvegarde vide avec en-tête si aucun n'existe."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin = os.path.join(script_dir, "..", "magasins/sauvegarde_rapide.csv")
        if not os.path.exists(chemin):
            with open(chemin, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(["Nom du projet", "Nom du produit", "X", "Y", "Position"])

    def charger_csv(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repertoire_defaut = os.path.join(script_dir, "..", "magasins/")
        fichier, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption="Choisissez le magasin où vous souhaitez aller",
            directory = repertoire_defaut,
            filter="Fichiers CSV (*.csv);;Tous les fichiers (*)"
            )

        if fichier:
            self.ouvrir_signal.emit(fichier)
            try:
                max_col = 0
                max_row = 0
                produits_csv = []  # Pour stocker les lignes de données
                with open(fichier, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    # Lecture de l'en-tête (si présent)
                    header = next(reader, None)
                    # Parcours des lignes de données
                    for row in reader:
                        if len(row) < 4:
                            # Ignorer les lignes incomplètes
                            continue
                        try:
                            # On attend que les colonnes 2 et 3 contiennent X et Y
                            x = int(row[2])
                            y = int(row[3])
                        except Exception as e:
                            print("Erreur de conversion dans la ligne :", row, e)
                            continue
                        max_col = max(max_col, x)
                        max_row = max(max_row, y)
                        produits_csv.append(row)
                
  
                new_cols = max_col +1
                new_rows = max_row +1
                print(f"Mise à jour du quadrillage avec {new_rows} lignes et {new_cols} colonnes")
                
                # Met à jour le quadrillage avec les nouvelles dimensions issues du CSV
                self.mettre_a_jour_grille(new_rows, new_cols)

                self.ouvrir_signal.emit(fichier)
            except Exception as e:
                print("Erreur lors du chargement du CSV :", e)

    def maj_nom_projet_csv(self, nouveau_nom):
        """
        Met à jour le CSV '../magasins/sauvegarde_rapide.csv' en modifiant la première colonne (Nom du projet)
        pour toutes les lignes, et ce en temps réel à chaque modification.
        """
        try:
            # Si le fichier existe, on le lit
            script_dir = os.path.dirname(os.path.abspath(__file__))
            chemin = os.path.join(script_dir, "..", "magasins/sauvegarde_rapide.csv")
            if os.path.exists(chemin):
                with open(chemin, "r", newline='', encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    lignes = list(reader)

            # Vérifier que le fichier contient au moins une ligne (l'en-tête)
            if len(lignes) > 0:
                en_tete = lignes[0]
                nouvelles_lignes = [en_tete]
                for ligne in lignes[1:]:
                    if len(ligne) >= 1:
                        ligne[0] = nouveau_nom
                    nouvelles_lignes.append(ligne)

        # Réécriture du fichier CSV avec les nouvelles valeurs
            with open(chemin, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerows(nouvelles_lignes)

        except Exception as e:
            print(f"[ERREUR] Lors de la mise à jour du CSV: {e}")

    def create_partie_gauche(self):
        """Crée la partie gauche de l'interface"""
        self.partie_gauche = QtWidgets.QWidget(self)
        self.partie_gauche.setMinimumWidth(200)
        self.partie_gauche.setStyleSheet("background-color: #232323; font-size: 16px; color: white;")
        
        layout = QtWidgets.QVBoxLayout(self.partie_gauche)
        
        # Section des articles
        self.create_articles()
        
        # Section du tableau de bord
        self.create_panier()
        
        layout.addWidget(self.liste_articles, stretch=1)
        layout.addWidget(self.panier, stretch=1)
        
        self.layout.addWidget(self.partie_gauche, stretch=1)
    
    def create_articles(self):
        """Crée la section de gestion des articles"""
        self.liste_articles = QtWidgets.QWidget(self.partie_gauche)
        self.liste_articles.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.liste_articles.setMinimumHeight(100)
        
        layout_articles = QtWidgets.QVBoxLayout(self.liste_articles)
        
        # Barre de recherche
        self.recherche_articles = QtWidgets.QLineEdit(self.liste_articles)
        self.recherche_articles.setPlaceholderText("Rechercher un article...")
        self.recherche_articles.setMinimumWidth(400)
        self.recherche_articles.setStyleSheet("padding: 5px; margin-left: 20px; margin-top: 20px;")
        
        # Zone scrollable pour les articles
        self.articles_box = QtWidgets.QWidget(self.liste_articles)
        self.layout_articles_box = QtWidgets.QVBoxLayout(self.articles_box)
        self.layout_articles_box.setContentsMargins(20, 20, 20, 140)
        self.layout_articles_box.setSpacing(10)
        
        scroll = QtWidgets.QScrollArea(self.liste_articles)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        scroll.setWidget(self.articles_box)

        # Boutons d'action
        layout_boutons = QtWidgets.QHBoxLayout()
        layout_boutons.setContentsMargins(10, 10, 10, 10)

        self.bouton_ouvrir = QtWidgets.QPushButton("Ouvrir", self.recherche_articles)
        self.bouton_effacer = QtWidgets.QPushButton("Effacer", self.liste_articles)

        layout_boutons.addWidget(self.bouton_ouvrir)
        layout_boutons.addWidget(self.bouton_effacer)

        for bouton in [self.bouton_ouvrir, self.bouton_effacer]:
            bouton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            bouton.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px; margin-bottom: 10px;")
            bouton.setMaximumWidth(200)
            bouton.setMaximumHeight(50)
        
        layout_articles.addWidget(self.recherche_articles, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft, stretch=1)
        layout_articles.addWidget(scroll, stretch=12)
        self.recherche_articles.textChanged.connect(self.on_recherche_changee)

        layout_articles.addLayout(layout_boutons)
    
    def on_recherche_changee(self, texte):
        """Lorsque le texte change"""
        self.recherche_changee.emit(texte)

    def filtrer_produits(self, produits, filtre):
        """filtre les produits selon l'etat de la barre de recherche"""
        if not filtre:
            return produits
        return [p for p in produits if filtre.lower() in p.lower()]
    
    def create_panier(self):
        """Crée la section du tableau de bord"""
        self.panier = QtWidgets.QWidget(self.partie_gauche)
        self.panier.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.panier.setMinimumHeight(100)
        self.panier.setContentsMargins(40, 0, 0, 0)
        
        # Layout principal du panier
        layout_panier_principal = QtWidgets.QVBoxLayout(self.panier)
        
        # Label titre
        self.label_panier = QtWidgets.QLabel("<i>Votre panier</i>", self.panier)
        layout_panier_principal.addWidget(self.label_panier, alignment=QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        # Créer la zone scrollable
        self.scroll_area = QtWidgets.QScrollArea(self.panier)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #2c2c2c; }")
        
        # Widget contenu pour le scroll
        self.widget_contenu_panier = QtWidgets.QWidget()
        self.widget_contenu_panier.setStyleSheet("background-color: #2c2c2c;")
        
        # Layout pour le contenu scrollable (c'est celui où vous ajouterez vos produits)
        self.layout_panier = QtWidgets.QVBoxLayout(self.widget_contenu_panier)
        self.layout_panier.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        
        # Connecter le widget contenu au scroll area
        self.scroll_area.setWidget(self.widget_contenu_panier)
        
        # Ajouter le scroll area au layout principal
        layout_panier_principal.addWidget(self.scroll_area)
            
    def create_partie_droite(self):
        """Crée la partie droite avec la grille et l'image du magazin"""
        self.partie_droite = QtWidgets.QWidget(self)
        self.partie_droite.setStyleSheet("background-color: #232323;")
        layout = QtWidgets.QVBoxLayout(self.partie_droite)
        
        # Header avec nom du magasin
        header = QtWidgets.QWidget(self.partie_droite)
        layout_header = QtWidgets.QHBoxLayout(header)
        layout_header.setContentsMargins(10, 10, 10, 10)
        layout_header.setSpacing(10)
        
        self.label = QtWidgets.QLabel("Votre magasin :", self.partie_droite)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.label.setStyleSheet("color: white; font-size: 16px;")
        
        self.nom_magasin = QtWidgets.QLineEdit(self.partie_droite)
        self.nom_magasin.setPlaceholderText("Nom du magasin")
        self.nom_magasin.setMinimumWidth(400)
        self.nom_magasin.setMaximumWidth(400)
        self.nom_magasin.setStyleSheet("padding: 5px;")
  
        
        layout_header.addWidget(self.label)
        layout_header.addWidget(self.nom_magasin)
        
        # légende1
        legend_container1 = QtWidgets.QWidget(self.partie_droite)
        legend_layout1 = QtWidgets.QHBoxLayout(legend_container1)
        legend_layout1.setContentsMargins(10, 0, 10, 10)
        legend_layout1.setSpacing(5)
        
        # Carré de couleur
        legend_color1 = QtWidgets.QFrame(legend_container1)
        legend_color1.setFixedSize(20, 20)
        legend_color1.setStyleSheet("background-color: rgba(100, 10, 10, 1); border: 1px solid black;")
        
        # Zone de texte
        legend_label = QtWidgets.QLabel("couloirs", legend_container1)
        legend_label.setStyleSheet("color: white; font-size: 14px;")
        
        legend_layout1.addWidget(legend_color1)
        legend_layout1.addWidget(legend_label)
        
        
        
            # Ajout de la légende2
        legend_container2 = QtWidgets.QWidget(self.partie_droite)
        legend_layout2 = QtWidgets.QHBoxLayout(legend_container2)
        legend_layout2.setContentsMargins(10, 0, 10, 10)
        legend_layout2.setSpacing(5)
        
        # Carré de couleur
        legend_color2 = QtWidgets.QFrame(legend_container2)
        legend_color2.setFixedSize(20, 20)
        legend_color2.setStyleSheet("background-color:  rgba(10, 100, 10, 1); border: 1px solid black;")
        
        # Zone de texte
        legend_label2 = QtWidgets.QLabel("rayons", legend_container2)
        legend_label2.setStyleSheet("color: white; font-size: 14px;")

        bouton_deconnection = QtWidgets.QPushButton("Se déconnecter")
        bouton_deconnection.setStyleSheet("padding: 5px; margin-left: 20px")
        bouton_deconnection.clicked.connect(self.fermer_et_connexion)

        
        legend_layout2.addWidget(legend_color2)
        legend_layout2.addWidget(legend_label2)

        bouton_deconnection = QtWidgets.QPushButton("Se déconnecter")
        bouton_deconnection.clicked.connect(self.on_bouton_deconnection)
        
        layout_header.addWidget(legend_container1)
        layout_header.addWidget(legend_container2)
        layout_header.addWidget(bouton_deconnection)
        
        # Zone du plan avec grille
        self.create_zone_plan()
        
        layout.addWidget(header, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.zone_superposee, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.partie_droite, stretch=1)
    
    def on_bouton_deconnection(self):
        """emmet le signal de deconnexion"""
        self.deconnexion_signal.emit()
    
    def create_zone_plan(self):
        """Crée la zone du plan avec la grille interactive"""
        self.zone_superposee = QtWidgets.QWidget(self.partie_droite)
        self.zone_superposee.setContentsMargins(0, 0, 0, 0)
        self.zone_superposee.setFixedSize(720, 900)
        self.zone_superposee.setStyleSheet("background-color: transparent;")
        
        # Image de fond
        self.label_plan = QtWidgets.QLabel(self.zone_superposee)
        self.label_plan.setGeometry(0, 0, 720, 900)
        
        transform = QTransform().rotate(90)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin = os.path.join(script_dir, "..", "plan_magasin.jpg")
        
        plan = QPixmap(chemin)
        if plan.isNull():
            print(f"Erreur : l'image n'a pas pu être chargée depuis {chemin}")
            plan = QPixmap(720, 900)
        
        plan = plan.transformed(transform)
        self.label_plan.setPixmap(plan)
        self.label_plan.setScaledContents(True)
        self.label_plan.setMaximumSize(760, 900)
        self.label_plan.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_plan.setStyleSheet("background-color: transparent;")
        
        # Grille interactive
        self.labels_grille = QtWidgets.QWidget(self.zone_superposee)
        self.labels_grille.setStyleSheet("background-color: transparent;")
        self.labels_grille.setGeometry(self.label_plan.geometry())
        self.labels_grille.resize(self.label_plan.width(), self.label_plan.height())
        
        self.cellules_grille = {}
        self.create_grille(52, 35)

    def colorier_cellule_en_orange(self, ligne, colonne):
        """Colorie une cellule graphique DropArea en orange à partir de ses coordonnées."""
        cellule = self.cellules_grille.get((ligne, colonne))
        if cellule:
            cellule.setStyleSheet("""
                background-color: orange;
                border: 2px solid black;
            """)
        else:
            print(f"[AVERTISSEMENT] Cellule ({ligne}, {colonne}) introuvable dans la grille.")
    
    def create_grille(self, rows, cols):
        """Crée la grille de cellules interactives"""
        # Nettoyer l'ancienne grille
        for cellule in self.cellules_grille.values():
            cellule.deleteLater()
        self.cellules_grille.clear()
        
        model = MagasinModel()
        cases_colorees = model.analyser_image(52, 35)
        self.graphe = Graphe(rows, cols, cases_colorees, parent=self.labels_grille)
        self.graphe.afficher_grille(self.labels_grille, self.cellules_grille)
        # Marquer l'entrée
        if self.position_actuelle in self.graphe.cellules_graphiques:
            self.graphe.cellules_graphiques[self.position_actuelle].marquer_comme_entree()
    
    def effacer_projet(self):
        """
        Réinitialise le fichier '../magasins/sauvegarde_rapide.csv', vide le contenu
        de toutes les cellules de la grille, efface le nom du projet dans le widget
        et supprime la popup active,
        """
        try:
            # Réinitialisation du CSV (en gardant l'en-tête)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            chemin = os.path.join(script_dir, "..", "magasins/sauvegarde_rapide.csv")
            with open(chemin, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(["Nom du projet", "Nom du produit", "X", "Y", "Position"])
            print("Fichier CSV réinitialisé avec succès.")
        except Exception as e:
            print(f"[ERREUR] Impossible de réinitialiser le CSV : {e}")

        # Effacer le contenu visuel de toutes les cellules de la grille (DropArea)
        for cell in self.labels_grille.findChildren(DropArea):
            cell.setText("")
            cell.setStyleSheet(cell.default_style)
            cell.articles = []  # Réinitialiser le contenu interne

        # Effacer le nom du projet affiché dans le widget
        self.nom_magasin.setText("")

        # Supprimer la popup active, si elle existe
        if hasattr(self, "popup_actuelle") and self.popup_actuelle:
            self.popup_actuelle.hide()
            self.popup_actuelle.deleteLater()
            self.popup_actuelle = None

        print("Contenu du projet, nom affiché et pop-up effacés. L'application reste ouverte.")
    
    def connecter_signaux(self):
        """Connecte les signaux internes"""
        self.nom_magasin.textChanged.connect(self.nom_magasin_change.emit)
        self.bouton_effacer.clicked.connect(self.effacer_projet)
        self.bouton_ouvrir.clicked.connect(self.charger_csv)
        self.nom_magasin.textChanged.connect(self.maj_nom_projet_csv)
        self.bouton_sauvegarder.clicked.connect(self.on_bouton_sauvegarder_clicked)

    def fermer_et_connexion(self):
        self.deconnecter_signal.emit()

    def on_placer_produit(self, ligne, colonne, produit):
        """Émet le signal de placement de produit"""
        self.placer_produit.emit(ligne, colonne, produit)

    def on_cellule_cliquee(self, ligne, colonne):
        """
        Gère le clic sur une cellule : recherche la DropArea correspondante dans la grille.
        Si la cellule possède des articles, affiche une popup avec le contenu.
        """
        for drop_area in self.labels_grille.findChildren(DropArea):
            if drop_area.ligne == ligne and drop_area.colonne == colonne:
                if drop_area.articles and len(drop_area.articles) > 0:
                    self.afficher_popup_articles(ligne, colonne, drop_area.articles)
                break

    def on_placer_produit(self, ligne, colonne, produit):
        """Émet le signal de placement de produit"""
        self.placer_produit.emit(ligne, colonne, produit)
    
    def create_grille(self, rows, cols):
        """Crée la grille de cellules interactives"""
        # Nettoyer l'ancienne grille
        for cellule in self.cellules_grille.values():
            cellule.deleteLater()
        self.cellules_grille.clear()
        
        model = ClientModel()
        cases_colorees = model.analyser_image(rows, cols)
        self.graphe = Graphe(rows, cols, cases_colorees, parent=self.labels_grille)
        self.graphe.afficher_grille(self.labels_grille)
        
        for (i, j), drop_area in self.graphe.cellules_graphiques.items():
            drop_area.placer_produit.connect(self.on_placer_produit)
            drop_area.cellule_cliquee.connect(self.on_cellule_cliquee)
            self.cellules_grille[(i, j)] = drop_area
    
    def connecter_signaux(self):
        """Connecte des signaux internes"""
        self.nom_magasin.textChanged.connect(self.nom_magasin_change.emit)
        self.bouton_ouvrir.clicked.connect(self.charger_csv)
        self.bouton_effacer.clicked.connect(self.on_bouton_fermer)
        self.nom_magasin.textChanged.connect(self.maj_nom_projet_csv)

    def fermer_et_connexion(self):
        self.deconnecter_signal.emit()

    def on_bouton_fermer(self):
        """emmet le signal pour effacer le panier"""
        self.effacer_signal.emit()

    def afficher_categories(self, categories):
        """Affiche la liste des catégories"""
        self.clear_layout(self.layout_articles_box)
        
        for categorie in categories:
            btn = QtWidgets.QPushButton(categorie, self.articles_box)
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(55)
            btn.setMinimumWidth(150)
            btn.clicked.connect(lambda checked, cat=categorie: self.categorie_cliquee.emit(cat))
            btn.setStyleSheet("background-color: #232323; border-radius: 5px; color: white; padding: 10px; margin-bottom: 10px;")
            self.layout_articles_box.addWidget(btn, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
    
    def afficher_produits(self, produits):
        """Affiche la liste des produits d'une catégorie"""
        self.clear_layout(self.layout_articles_box)
        
        # Bouton retour
        btn_retour = QtWidgets.QPushButton("← Retour", self.articles_box)
        btn_retour.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_retour.setFixedHeight(40)
        btn_retour.setMaximumWidth(150)
        btn_retour.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px; margin-bottom: 10px;")
        btn_retour.clicked.connect(self.retour_categories.emit)
        self.layout_articles_box.addWidget(btn_retour)
        
        for produit in produits:
            btn_produit = QtWidgets.QPushButton(produit, self.articles_box)
            btn_produit.setStyleSheet("background-color: #232323; padding: 10px;")
            btn_produit.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn_produit.clicked.connect(self.on_produit_clique)
            self.layout_articles_box.addWidget(btn_produit, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        
        self.articles_box.adjustSize()
        self.articles_box.update()

    def on_produit_clique(self):
        """emmet le signal d'un produit"""
        bouton_clique = self.sender()
        if isinstance(bouton_clique, QtWidgets.QPushButton):
            texte_produit = bouton_clique.text()
            self.produit_signal.emit(texte_produit)

    def ajouter_produit(self, nom_produit):
        """ajoute un produit au panier"""
        btn = QtWidgets.QPushButton(nom_produit)
        btn.setStyleSheet("max-width: 200px")
        btn.clicked.connect(lambda checked: self.enlever_produit_panier())
        self.layout_panier.addWidget(btn, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignCenter)

    def enlever_produit_panier(self):
        """emmet le signal de suppression"""
        bouton_clique = self.sender()
        if isinstance(bouton_clique, QtWidgets.QPushButton):
            texte_produit = bouton_clique.text()
            print(f"[DEBUG] Émission du signal avec : '{texte_produit}' (type: {type(texte_produit)})")
            self.enlever_produit_signal.emit(texte_produit)
    
    def enlever_produit(self, nom_produit):
        """Méthode pour enlever un produit par son nom"""
        print(f"[DEBUG] Signal reçu : '{nom_produit}' (type: {type(nom_produit)})")
        
        for i in range(self.layout_panier.count() - 1, -1, -1):
            item = self.layout_panier.itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, QtWidgets.QPushButton) and widget.text() == nom_produit:
                    print(f"[DEBUG] Widget trouvé, suppression...")
                    self.layout_panier.removeWidget(widget)
                    widget.deleteLater()
                    return
        
        print(f"[DEBUG] Aucun widget trouvé avec le nom '{nom_produit}'")
    
    def clear_layout(self, layout):
        """Vide un layout de tous ses widgets"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
            
class DraggableLabel(QtWidgets.QLabel):
    """Label draggable pour les produits"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        self.setMaximumWidth(300)
        self.setStyleSheet("color: white; background-color: #333; padding: 5px; border-radius: 3px;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            mimeData = QtCore.QMimeData()
            mimeData.setText(self.text())
            
            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            
            pixmap = self.grab()
            drag.setPixmap(pixmap)
            drag.setHotSpot(QtCore.QPoint(0, 0))
            
            drag.exec(QtCore.Qt.DropAction.MoveAction)