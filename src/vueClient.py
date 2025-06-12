from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QFileDialog
from graphe import Graphe
from droparea import DropArea
from modelAdmin import MagasinModel
import os
import csv

class VueClient(QtWidgets.QWidget):
    """Vue principale de l'interface administrateur"""
    
    # Signaux pour communiquer avec le contrôleur
    categorie_cliquee = QtCore.pyqtSignal(str)
    produit_ajoute = QtCore.pyqtSignal(str)
    retour_categories = QtCore.pyqtSignal()
    cellule_cliquee = QtCore.pyqtSignal(int, int)
    dimensions_changees = QtCore.pyqtSignal(int, int)  # colonnes, lignes
    nom_magasin_change = QtCore.pyqtSignal(str)
    placer_produit = QtCore.pyqtSignal(int, int, str)  # ligne, colonne, produit
    recherche_changee = QtCore.pyqtSignal(str)

    def __init__(self):
        """Initialise l'interface utilisateur"""
        super(VueClient, self).__init__()
        self.setWindowTitle("Créateur de magazin Administrateur")
        self.setGeometry(200, 200, 1600, 1200)
        
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Dictionnaire pour stocker la liste de courses organisée par catégories
        self.liste_courses = {}
        # Mapping des produits vers leurs catégories
        self.produits_categories = {}
        
        self.create_partie_gauche()
        self.create_partie_droite()
        
        self.connecter_signaux()

        self.popup_actuelle = None
    
    def definir_categories_produits(self, categories_produits):
        """Définit le mapping entre produits et catégories"""
        self.produits_categories.clear()
        for categorie, produits in categories_produits.items():
            for produit in produits:
                self.produits_categories[produit] = categorie
    
    def ajouter_a_liste_courses(self, produit):
        """Ajoute un produit à la liste de courses, organisé par catégorie"""
        if produit in self.produits_categories:
            categorie = self.produits_categories[produit]
            
            if categorie not in self.liste_courses:
                self.liste_courses[categorie] = []
            
            if produit not in self.liste_courses[categorie]:
                self.liste_courses[categorie].append(produit)
                self.mettre_a_jour_affichage_liste_courses()
    
    def retirer_de_liste_courses(self, produit, categorie):
        """Retire un produit de la liste de courses"""
        if categorie in self.liste_courses and produit in self.liste_courses[categorie]:
            self.liste_courses[categorie].remove(produit)
            if not self.liste_courses[categorie]:  # Si la catégorie est vide
                del self.liste_courses[categorie]
            self.mettre_a_jour_affichage_liste_courses()
    
    def mettre_a_jour_affichage_liste_courses(self):
        """Met à jour l'affichage de la liste de courses"""
        # Vider le widget actuel
        self.clear_layout(self.layout_liste_courses)
        
        if not self.liste_courses:
            label_vide = QtWidgets.QLabel("Liste de courses vide\nCliquez sur un produit pour l'ajouter")
            label_vide.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_vide.setStyleSheet("color: #888; font-style: italic; padding: 20px;")
            self.layout_liste_courses.addWidget(label_vide)
            return
        
        # Afficher les catégories et leurs produits
        for categorie in sorted(self.liste_courses.keys()):
            # Titre de la catégorie
            titre_categorie = QtWidgets.QLabel(f"📦 {categorie}")
            titre_categorie.setStyleSheet("""
                font-weight: bold; 
                font-size: 14px; 
                color: #4CAF50; 
                padding: 5px 0px; 
                border-bottom: 1px solid #555;
                margin-top: 10px;
            """)
            self.layout_liste_courses.addWidget(titre_categorie)
            
            # Produits de la catégorie
            for produit in sorted(self.liste_courses[categorie]):
                widget_produit = QtWidgets.QWidget()
                layout_produit = QtWidgets.QHBoxLayout(widget_produit)
                layout_produit.setContentsMargins(10, 2, 5, 2)
                
                # Label du produit
                label_produit = QtWidgets.QLabel(f"• {produit}")
                label_produit.setStyleSheet("color: white; padding: 2px 0px;")
                
                # Bouton de suppression
                btn_supprimer = QtWidgets.QPushButton("✕")
                btn_supprimer.setFixedSize(20, 20)
                btn_supprimer.setStyleSheet("""
                    QPushButton {
                        background-color: #ff4444;
                        color: white;
                        border: none;
                        border-radius: 10px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #ff6666;
                    }
                """)
                btn_supprimer.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                btn_supprimer.clicked.connect(lambda checked, p=produit, c=categorie: self.retirer_de_liste_courses(p, c))
                
                layout_produit.addWidget(label_produit)
                layout_produit.addStretch()
                layout_produit.addWidget(btn_supprimer)
                
                self.layout_liste_courses.addWidget(widget_produit)
        
        # Spacer pour pousser le contenu vers le haut
        self.layout_liste_courses.addStretch()
    
    def effacer_liste_courses(self):
        """Efface toute la liste de courses"""
        self.liste_courses.clear()
        self.mettre_a_jour_affichage_liste_courses()
    
    def afficher_popup_articles(self, ligne, colonne, articles):
        """Affiche une popup avec les articles d'une cellule"""
        if not articles:
            return
        
        # Fermer la popup existante
        if self.popup_actuelle:
            self.popup_actuelle.hide()
            self.popup_actuelle.deleteLater()
        
        # Créer et afficher la nouvelle popup
        popup = self.creer_popup_articles(articles)
        popup.show()
        self.popup_actuelle = popup

    def creer_popup_articles(self, articles):
        """Crée une popup pour afficher les articles d'une cellule"""
        popup = QtWidgets.QWidget(self)
        popup.setWindowFlags(QtCore.Qt.WindowType.Popup)
        popup.setStyleSheet("""
            background-color: #2c2c2c;
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
        """)
        
        layout = QtWidgets.QVBoxLayout(popup)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Titre de la popup
        titre = QtWidgets.QLabel("Articles dans cette case:", popup)
        titre.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titre)
        
        # Liste des articles
        for article in articles:
            label = QtWidgets.QLabel(article, popup)
            label.setStyleSheet("padding: 5px;")
            layout.addWidget(label)
        
        # Ajuster la taille de la popup
        popup.adjustSize()
        
        # Positionner la popup au centre de l'écran
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        popup_width = popup.width()
        popup_height = popup.height()
        
        # Calculer la position centrale
        x = (screen.width() - popup_width) // 2
        y = (screen.height() - popup_height) // 2
        
        popup.move(x, y)
        
        return popup

    def create_partie_gauche(self):
        """Crée la partie gauche de l'interface"""
        self.partie_gauche = QtWidgets.QWidget(self)
        self.partie_gauche.setMinimumWidth(200)
        self.partie_gauche.setStyleSheet("background-color: #232323; font-size: 16px; color: white;")
        
        layout = QtWidgets.QVBoxLayout(self.partie_gauche)
        
        # Section des articles
        self.create_articles()
        
        # Section de la liste de courses (remplace le tableau de bord)
        self.create_liste_courses()
        
        layout.addWidget(self.liste_articles, stretch=2)
        layout.addWidget(self.widget_liste_courses, stretch=1)
        
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
    
    def create_liste_courses(self):
        """Crée la section de la liste de courses"""
        self.widget_liste_courses = QtWidgets.QWidget(self.partie_gauche)
        self.widget_liste_courses.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.widget_liste_courses.setMinimumHeight(100)
        self.widget_liste_courses.setContentsMargins(20, 10, 20, 10)
        
        layout_principal = QtWidgets.QVBoxLayout(self.widget_liste_courses)
        
        # Titre de la section
        titre_liste = QtWidgets.QLabel("🛒 Liste de courses")
        titre_liste.setStyleSheet("font-weight: bold; font-size: 16px; color: #4CAF50; margin-bottom: 10px;")
        layout_principal.addWidget(titre_liste)
        
        # Zone scrollable pour la liste de courses
        self.scroll_liste_courses = QtWidgets.QScrollArea()
        self.scroll_liste_courses.setWidgetResizable(True)
        self.scroll_liste_courses.setStyleSheet("border: none; background-color: #333;")
        
        self.widget_contenu_liste = QtWidgets.QWidget()
        self.layout_liste_courses = QtWidgets.QVBoxLayout(self.widget_contenu_liste)
        self.layout_liste_courses.setContentsMargins(10, 10, 10, 10)
        self.layout_liste_courses.setSpacing(5)
        
        self.scroll_liste_courses.setWidget(self.widget_contenu_liste)
        
        # Boutons d'action (comme dans l'ancien tableau de bord)
        layout_boutons = QtWidgets.QHBoxLayout()
        layout_boutons.setContentsMargins(0, 10, 0, 10)
        
        self.bouton_ouvrir = QtWidgets.QPushButton("Ouvrir", self.widget_liste_courses)
        self.bouton_sauvegarder = QtWidgets.QPushButton("Sauvegarder", self.widget_liste_courses)
        self.bouton_effacer = QtWidgets.QPushButton("Effacer", self.widget_liste_courses)
        
        for bouton in [self.bouton_ouvrir, self.bouton_sauvegarder, self.bouton_effacer]:
            bouton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            bouton.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px; margin: 2px;")
            bouton.setMaximumWidth(80)
            bouton.setMaximumHeight(30)
        
        # Connecter le bouton effacer à la fonction de nettoyage de la liste
        self.bouton_effacer.clicked.connect(self.effacer_liste_courses)
        
        layout_boutons.addWidget(self.bouton_ouvrir)
        layout_boutons.addWidget(self.bouton_sauvegarder)
        layout_boutons.addWidget(self.bouton_effacer)
        
        layout_principal.addWidget(self.scroll_liste_courses)
        layout_principal.addLayout(layout_boutons)
        
        # Initialiser l'affichage
        self.mettre_a_jour_affichage_liste_courses()
    
    def on_recherche_changee(self, texte):
        """Lorsque le texte change"""
        self.recherche_changee.emit(texte)

    def filtrer_produits(self, produits, filtre):
        """filtre les produits selon l'etat de la barre de recherche"""
        if not filtre:
            return produits
        return [p for p in produits if filtre.lower() in p.lower()]
    
    def create_partie_droite(self):
        """Crée la partie droite avec la grille et l'image du magazin"""
        self.partie_droite = QtWidgets.QWidget(self)
        self.partie_droite.setStyleSheet("background-color: #00000000;")
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
        
        # Zone du plan avec grille
        self.create_zone_plan()
        
        layout.addWidget(header, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.zone_superposee, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.partie_droite, stretch=1)
    
    def create_zone_plan(self):
        """Crée la zone du plan avec la grille interactive"""
        self.zone_superposee = QtWidgets.QWidget(self.partie_droite)
        self.zone_superposee.setContentsMargins(0, 0, 0, 0)
        self.zone_superposee.setFixedSize(760, 900)
        self.zone_superposee.setStyleSheet("background-color: transparent;")
        
        # Image de fond
        self.label_plan = QtWidgets.QLabel(self.zone_superposee)
        self.label_plan.setGeometry(0, 0, 760, 900)
        
        transform = QTransform().rotate(90)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin = os.path.join(script_dir, "..", "plan_magasin.jpg")
        
        plan = QPixmap(chemin)
        if plan.isNull():
            print(f"Erreur : l'image n'a pas pu être chargée depuis {chemin}")
            plan = QPixmap(760, 900)
        
        plan = plan.transformed(transform)
        self.label_plan.setPixmap(plan)
        self.label_plan.setScaledContents(True)
        self.label_plan.setMaximumSize(760, 900)
        self.label_plan.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_plan.setStyleSheet("background-color: transparent;")
        
        # Grille interactive
        self.labels_grille = QtWidgets.QWidget(self.zone_superposee)
        self.labels_grille.setStyleSheet("background-color: #00000000;")
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
    
    def connecter_signaux(self):
        """Connecte les signaux internes"""
        self.nom_magasin.textChanged.connect(self.nom_magasin_change.emit)
    
    def on_dimensions_changees(self):
        """Émet le signal de changement de dimensions"""
        self.dimensions_changees.emit(self.spinTableauBordColonnes.value(), self.spinTableauBordLignes.value())
    
    def on_placer_produit(self, ligne, colonne, produit):
        """Émet le signal de placement de produit"""
        self.placer_produit.emit(ligne, colonne, produit)

    def on_cellule_cliquee(self, ligne, colonne):
        """Gère le clic sur une cellule"""
        self.cellule_cliquee.emit(ligne, colonne)
    
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
        
        # Produits draggables avec clic gauche
        for produit in produits:
            label = DraggableLabel(produit, self.articles_box)
            # Connecter le signal de clic gauche
            label.produit_clique.connect(self.ajouter_a_liste_courses)
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
        self.create_grille(rows, cols)
    
    def effacer_grille(self):
        """Efface tous les produits de la grille"""
        for cellule in self.cellules_grille.values():
            cellule.setText("")
            cellule.setStyleSheet("background-color: #00000000;")


class DraggableLabel(QtWidgets.QLabel):
    """Label draggable pour les produits avec support du clic gauche"""
    
    # Signal émis quand on clique gauche sur le produit
    produit_clique = QtCore.pyqtSignal(str)
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        self.setMaximumWidth(300)
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }
            QLabel:hover {
                background-color: #444;
                border-color: #4CAF50;
            }
        """)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # Stocker la position du clic pour détecter le drag plus tard
            self.click_position = event.position()
            self.drag_started = False
    
    def mouseMoveEvent(self, event):
        # Si la souris bouge suffisamment, commencer le drag
        if (event.buttons() == QtCore.Qt.MouseButton.LeftButton and 
            hasattr(self, 'click_position') and not hasattr(self, 'drag_started')):
            
            distance = (event.position() - self.click_position).manhattanLength()
            
            # Si on bouge la souris de plus de 5 pixels, commencer le drag
            if distance > 5:
                self.drag_started = True
                mimeData = QtCore.QMimeData()
                mimeData.setText(self.text())
                
                drag = QtGui.QDrag(self)
                drag.setMimeData(mimeData)
                
                pixmap = self.grab()
                drag.setPixmap(pixmap)
                drag.setHotSpot(QtCore.QPoint(0, 0))
                
                drag.exec(QtCore.Qt.DropAction.MoveAction)
    
    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.MouseButton.LeftButton and 
            hasattr(self, 'click_position') and 
            not getattr(self, 'drag_started', False)):
            
            # C'était un simple clic, émettre le signal
            self.produit_clique.emit(self.text())
        
        # Nettoyer les attributs temporaires
        if hasattr(self, 'click_position'):
            delattr(self, 'click_position')
        if hasattr(self, 'drag_started'):
            delattr(self, 'drag_started')
        
        super().mouseReleaseEvent(event)