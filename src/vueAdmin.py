from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QFileDialog
from graphe import Graphe
from droparea import DropArea
from modelAdmin import MagasinModel
import os
import csv
from collections import Counter

class VueAdmin(QtWidgets.QWidget):
    """Vue principale de l'interface administrateur"""
    
    # Signaux pour communiquer avec le contrôleur
    categorie_cliquee = QtCore.pyqtSignal(str)
    retour_categories = QtCore.pyqtSignal()
    cellule_cliquee = QtCore.pyqtSignal(int, int)
    nombre_ligne_changee = QtCore.pyqtSignal(int)
    nombre_colonne_changee = QtCore.pyqtSignal(int)
    nom_magasin_change = QtCore.pyqtSignal(str)
    placer_produit = QtCore.pyqtSignal(int, int, str)  # ligne, colonne, produit
    recherche_changee = QtCore.pyqtSignal(str)
    sauvegarder_signal = QtCore.pyqtSignal()
    bouton_popup_signal = QtCore.pyqtSignal(int, int, str)

    def __init__(self):
        """Initialise l'interface utilisateur"""
        super(VueAdmin, self).__init__()
        self.setWindowTitle("Créateur de magazin Administrateur")
        self.setGeometry(200, 200, 1600, 1200)
        
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.create_partie_gauche()
        self.create_partie_droite()
        
        self.sauvegarder_signal.connect(self.sauvegarder_tous_les_produits)
        self.connecter_signaux()

        
        
        
         # Initialiser le fichier de sauvegarde s'il n'existe pas.
        self.initialiser_sauvegarde()
        self.popup_actuelle = None
    
    
    def initialiser_sauvegarde(self):
        """Crée un fichier de sauvegarde vide avec en-tête si aucun n'existe."""
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin = os.path.join(script_dir, "..", "magasins/sauvegarde_rapide.jpg")
        if not os.path.exists(chemin):
            with open(chemin, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(["Nom du projet", "Nom du produit", "X", "Y", "Position"])

    def charger_csv(self):
        """
        Ouvre une boîte de dialogue pour permettre à l'utilisateur de choisir un fichier CSV.
        Met à jour les DropAreas en fonction du contenu du fichier sélectionné.
        
        Le fichier CSV doit comporter 5 colonnes, dans cet ordre :
        - Nom du projet
        - Nom du produit
        - Colonne (numérique, en 1-base)
        - Ligne (numérique, en 1-base)
        - Position (optionnel : par exemple "A1")
        
        Pour chaque ligne, cette méthode convertit la colonne et la ligne en indices 0 base,
        recherche la DropArea correspondante, et met à jour son texte, son style (background)
        et son contenu.
        """

        chemin_fichier, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier CSV", "", "Fichiers CSV (*.csv)"
        )

        if not chemin_fichier:
            return
        try:
            with open(chemin_fichier, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=";")
                header = next(reader, None)  # Ignorer l'en-tête
                project_name = None

                for row in reader:
                    if len(row) < 5:
                        continue
                    nom_projet, produit, col_str, ligne_str, position = row

                    if project_name is None:
                        project_name = nom_projet

                    try:
                        col_index = int(col_str)   # On suppose ici que les valeurs sont déjà en 0-base
                        row_index = int(ligne_str)
                    except ValueError:
                        continue

                    for drop_area in self.labels_grille.findChildren(DropArea):
                        if drop_area.colonne == col_index and drop_area.ligne == row_index:
                            if produit.strip():
                                # Si des produits sont déjà présents, on ajoute le nouveau
                                if hasattr(drop_area, "articles") and drop_area.articles:
                                    drop_area.articles.append(produit)
                                else:
                                    drop_area.articles = [produit]
                                # Met à jour le texte affiché en joignant les produits par une virgule
                                drop_area.setText(", ".join(drop_area.articles))
                                drop_area.setStyleSheet(drop_area.filled_style)
                            else:
                                drop_area.setText("")
                                drop_area.setStyleSheet(drop_area.default_style)
                                drop_area.articles = []
                            break
                if project_name:
                    self.nom_magasin.setText(project_name)
                print(f"Chargement terminé : {chemin_fichier}")
        except Exception as e:
            print(f"[ERREUR] lors du chargement : {e}")

    def maj_nom_projet_csv(self, nouveau_nom):
        """
        Met à jour le CSV '../magasins/sauvegarde_rapide.csv' en modifiant la première colonne (Nom du projet)
        pour toutes les lignes, et ce en temps réel à chaque modification.
        """
        try:
            # Si le fichier existe, on le lit
            script_dir = os.path.dirname(os.path.abspath(__file__))
            chemin = os.path.join(script_dir, "..", "magasins/sauvegarde_rapide.jpg")
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
    
    
    def afficher_popup_articles(self, ligne, colonne, articles):
        """Affiche une popup listant les articles d'une cellule cliquée."""
        if not articles:
            return

        if self.popup_actuelle:
            self.popup_actuelle.hide()
            self.popup_actuelle.deleteLater()

        popup = self.creer_popup_articles(articles, ligne, colonne)
        popup.show()
        self.popup_actuelle = popup

    def creer_popup_articles(self, articles, ligne, colonne):
        try:
            if not isinstance(articles, list):
                print("Erreur : 'articles' n'est pas une liste")
                return None

            popup = QtWidgets.QWidget(self)
            popup.setWindowFlags(QtCore.Qt.WindowType.Popup)
            popup.setStyleSheet("""
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
            """)
            popup.setMinimumHeight(100)

            layout = QtWidgets.QVBoxLayout(popup)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(5)

            titre = QtWidgets.QLabel("Articles dans cette case :", popup)
            titre.setStyleSheet("font-weight: bold; font-size: 14px;")
            titre.setMaximumHeight(50)
            layout.addWidget(titre)

            from collections import Counter
            compte_articles = Counter(articles)

            for produit, quantite in compte_articles.items():
                texte = f"{produit} x{quantite}" if quantite > 1 else str(produit)
                bouton_popup = QtWidgets.QPushButton(texte, popup)
                bouton_popup.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                bouton_popup.setStyleSheet("padding: 5px;")

                def create_slot(bouton, produit=produit):
                    def slot():
                        self.bouton_popup_signal.emit(ligne, colonne, produit)
                        layout.removeWidget(bouton)
                        bouton.deleteLater()

                        if layout.count() <= 1:
                            popup.close()
                    return slot

                bouton_popup.clicked.connect(create_slot(bouton_popup))
                layout.addWidget(bouton_popup)

            popup.adjustSize()
            screen = QtWidgets.QApplication.primaryScreen().geometry()
            popup.move((screen.width() - popup.width()) // 2, (screen.height() - popup.height()) // 2)
            return popup

        except Exception as e:
            print("Erreur dans creer_popup_articles :", e)
            return None
    
    def debug_emit(self, l, c, p):
        print(f"[DEBUG VUE] Suppression demandée : {p} à ({l}, {c})")
        self.bouton_popup_signal.emit(l, c, p)

    def create_partie_gauche(self):
        """Crée la partie gauche de l'interface"""
        self.partie_gauche = QtWidgets.QWidget(self)
        self.partie_gauche.setMinimumWidth(200)
        self.partie_gauche.setStyleSheet("background-color: #232323; font-size: 16px; color: white;")
        
        layout = QtWidgets.QVBoxLayout(self.partie_gauche)
        
        # Section des articles
        self.create_articles()
        
        # Section du tableau de bord
        self.create_tableau_bord()
        
        layout.addWidget(self.liste_articles, stretch=2)
        layout.addWidget(self.tableau_de_bord, stretch=1)
        
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
        
        layout_articles.addWidget(self.recherche_articles, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft, stretch=1)
        layout_articles.addWidget(scroll, stretch=12)
        self.recherche_articles.textChanged.connect(self.on_recherche_changee)
    
    def on_recherche_changee(self, texte):
        """Lorsque le texte change"""
        self.recherche_changee.emit(texte)

    def filtrer_produits(self, produits, filtre):
        """filtre les produits selon l'etat de la barre de recherche"""
        if not filtre:
            return produits
        return [p for p in produits if filtre.lower() in p.lower()]
    
    def create_tableau_bord(self):
        """Crée la section du tableau de bord"""
        self.tableau_de_bord = QtWidgets.QWidget(self.partie_gauche)
        self.tableau_de_bord.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.tableau_de_bord.setMinimumHeight(100)
        self.tableau_de_bord.setContentsMargins(40, 0, 0, 0)
        
        layout_tableau_bord = QtWidgets.QVBoxLayout(self.tableau_de_bord)
        
        self.label_tableau_bord = QtWidgets.QLabel("Réglages du magasin", self.tableau_de_bord)
        
        # Contrôles pour les colonnes
        layout_colonnes = QtWidgets.QHBoxLayout()
        self.spinTableauBordColonnes = QtWidgets.QSpinBox(self.tableau_de_bord)
        self.spinTableauBordColonnes.setRange(1, 50)
        self.spinTableauBordColonnes.setValue(35)
        self.spinTableauBordColonnes.setStyleSheet("max-width: 70px;")
        label_colonnes = QtWidgets.QLabel("Nombre de colonnes visibles", self.tableau_de_bord)
        
        layout_colonnes.addWidget(self.spinTableauBordColonnes)
        layout_colonnes.addWidget(label_colonnes)
        
        # Contrôles pour les lignes
        layout_lignes = QtWidgets.QHBoxLayout()
        self.spinTableauBordLignes = QtWidgets.QSpinBox(self.tableau_de_bord)
        self.spinTableauBordLignes.setRange(1, 60)
        self.spinTableauBordLignes.setValue(52)
        self.spinTableauBordLignes.setStyleSheet("max-width: 70px;")
        label_lignes = QtWidgets.QLabel("Nombre de lignes visibles", self.tableau_de_bord)
        
        layout_lignes.addWidget(self.spinTableauBordLignes)
        layout_lignes.addWidget(label_lignes)
        
        # Boutons d'action
        layout_boutons = QtWidgets.QHBoxLayout()
        layout_boutons.setContentsMargins(10, 10, 10, 10)
        
        self.bouton_ouvrir = QtWidgets.QPushButton("Ouvrir", self.tableau_de_bord)
        self.bouton_sauvegarder = QtWidgets.QPushButton("Sauvegarder", self.tableau_de_bord)
        self.bouton_effacer = QtWidgets.QPushButton("Effacer", self.tableau_de_bord)
        
        for bouton in [self.bouton_ouvrir, self.bouton_sauvegarder, self.bouton_effacer]:
            bouton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            bouton.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px; margin-bottom: 10px;")
            bouton.setMaximumWidth(200)
            bouton.setMaximumHeight(50)
        
        layout_boutons.addWidget(self.bouton_ouvrir)
        layout_boutons.addWidget(self.bouton_sauvegarder)
        layout_boutons.addWidget(self.bouton_effacer)
        
        # Ajout des layout au tableau de bord
        layout_tableau_bord.addWidget(self.label_tableau_bord)
        layout_tableau_bord.addLayout(layout_colonnes)
        layout_tableau_bord.addLayout(layout_lignes)
        layout_tableau_bord.addLayout(layout_boutons)
            
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
        
            # Ajout de la légende1
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
        
        legend_layout2.addWidget(legend_color2)
        legend_layout2.addWidget(legend_label2)
        
        layout_header.addWidget(legend_container1)
        layout_header.addWidget(legend_container2)
        
        # Zone du plan avec grille
        self.create_zone_plan()
        
        layout.addWidget(header, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.zone_superposee, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.partie_droite, stretch=1)
    
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
    
    def create_grille(self, rows, cols):
        """Crée la grille de cellules interactives"""
        # Nettoyer l'ancienne grille
        for cellule in self.cellules_grille.values():
            cellule.deleteLater()
        self.cellules_grille.clear()
        
        model = MagasinModel()
        cases_colorees = model.analyser_image(rows, cols)
        self.graphe = Graphe(rows, cols, cases_colorees, parent=self.labels_grille)
        self.graphe.afficher_grille(self.labels_grille)
        
        for (i, j), drop_area in self.graphe.cellules_graphiques.items():
            drop_area.placer_produit.connect(self.on_placer_produit)
            drop_area.cellule_cliquee.connect(self.on_cellule_cliquee)
            self.cellules_grille[(i, j)] = drop_area
            
    def effacer_projet(self):
        """
        Réinitialise le fichier '../magasins/sauvegarde_rapide.csv', vide le contenu
        de toutes les cellules de la grille, efface le nom du projet dans le widget
        et supprime la popup active,
        """
        try:
            # Réinitialisation du CSV (en gardant l'en-tête)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            chemin = os.path.join(script_dir, "..", "magasins/sauvegarde_rapide.jpg")
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
    
    def on_bouton_sauvegarder_clicked(self):
        """Slot appelé lorsqu'on clique sur le bouton Sauvegarder."""
        try:
            self.sauvegarder_signal.emit()
            print("Signal de sauvegarde émis.")
        except Exception as e:
          
            print(f"[ERREUR] lors du clic sur le bouton Sauvegarder: {e}")
        
    def supprimer_article_cellule(self, ligne, colonne, produit):
        """Supprime un article d'une cellule DropArea spécifique"""
        for drop_area in self.labels_grille.findChildren(DropArea):
            if drop_area.ligne == ligne and drop_area.colonne == colonne:
                if produit in drop_area.articles:
                    drop_area.articles.remove(produit)
            drop_area.mettre_a_jour_apparence()

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
        
        # Produits draggables
        for produit in produits:
            label = DraggableLabel(produit, self.articles_box)
            self.layout_articles_box.addWidget(label)
        
        self.articles_box.adjustSize()
        self.articles_box.update()
    
    def clear_layout(self, layout):
        """Vide un layout de tous ses widgets"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def mettre_a_jour_grille(self, rows, cols):
        """Met à jour la grille avec de nouvelles dimensions"""
        if rows is not None:
            self.rows = rows
        if cols is not None:
            self.cols = cols
        self.create_grille(rows, cols)
    
    def effacer_grille(self):
        """Efface tous les produits de la grille"""
        for cellule in self.cellules_grille.values():
            cellule.setText("")
            cellule.setStyleSheet("border: 1px solid rgba(0, 0, 0, 0.8); background-color: #00000000;")

    def sauvegarder_tous_les_produits(self):
        """
        Ouvre un explorateur de fichiers pour permettre à l'utilisateur
        de choisir où sauvegarder les données de la grille au format CSV.
        """
        # Ouvre le dialogue pour choisir le fichier
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer la disposition du magasin",
            "disposition_magasin.csv",  # nom par défaut
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )

        # Si l'utilisateur annule, on quitte la méthode
        if not file_path:
            print("[INFO] Sauvegarde annulée par l'utilisateur.")
            return

        header = ["Nom du projet", "Nom du produit", "X", "Y", "Position"]
        nom_projet = self.nom_magasin.text() if hasattr(self, "nom_magasin") else ""

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(header)

                # Parcourir toutes les cellules de la grille
                for drop_area in self.labels_grille.findChildren(DropArea):
                    if hasattr(drop_area, "articles") and drop_area.articles:
                        produit_counts = Counter(drop_area.articles)
                        x, y = drop_area.colonne, drop_area.ligne
                        coord_formatee = f"{x}{y}"
                        for prod, quantite in produit_counts.items():
                            produit_str = f"{prod} x{quantite}" if quantite > 1 else prod
                            writer.writerow([nom_projet, produit_str, x, y, coord_formatee])
                    else:
                        produit = drop_area.text().strip()
                        if produit:
                            x, y = drop_area.colonne, drop_area.ligne
                            coord_formatee = f"{x}{y}"
                            writer.writerow([nom_projet, produit, x, y, coord_formatee])

            print(f"[INFO] Tous les produits ont été sauvegardés dans : {file_path}")
        except Exception as e:
            print(f"[ERREUR] Problème lors de la sauvegarde des produits : {e}")
        
            
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
