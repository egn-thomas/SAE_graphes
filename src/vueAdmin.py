from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
from graphe import Graphe
from droparea import DropArea
import os


class VueAdmin(QtWidgets.QWidget):
    """Vue principale de l'interface administrateur"""
    
    # Signaux pour communiquer avec le contrôleur
    categorie_cliquee = QtCore.pyqtSignal(str)
    retour_categories = QtCore.pyqtSignal()
    cellule_cliquee = QtCore.pyqtSignal(int, int)
    dimensions_changees = QtCore.pyqtSignal(int, int)  # colonnes, lignes
    nom_magasin_change = QtCore.pyqtSignal(str)
    placer_produit = QtCore.pyqtSignal(int, int, str)  # ligne, colonne, produit
    recherche_changee = QtCore.pyqtSignal(str)

    def __init__(self):
        """Initialise l'interface utilisateur"""
        super(VueAdmin, self).__init__()
        self.setWindowTitle("Créateur de magazin Administrateur")
        self.setGeometry(200, 200, 1600, 1200)
        
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.create_partie_gauche()
        self.create_partie_droite()
        
        self.connecter_signaux()

        self.popup_actuelle = None
    
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
        self.spinTableauBordColonnes.setRange(0, 50)
        self.spinTableauBordColonnes.setValue(35)
        self.spinTableauBordColonnes.setStyleSheet("max-width: 70px;")
        label_colonnes = QtWidgets.QLabel("Nombre de colonnes visibles", self.tableau_de_bord)
        
        layout_colonnes.addWidget(self.spinTableauBordColonnes)
        layout_colonnes.addWidget(label_colonnes)
        
        self.curseurTableauBordColonnes = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.tableau_de_bord)
        self.curseurTableauBordColonnes.setRange(0, 50)
        self.curseurTableauBordColonnes.setValue(35)
        self.curseurTableauBordColonnes.setStyleSheet("margin-bottom: 40px; max-width: 400px;")
        
        # Contrôles pour les lignes
        layout_lignes = QtWidgets.QHBoxLayout()
        self.spinTableauBordLignes = QtWidgets.QSpinBox(self.tableau_de_bord)
        self.spinTableauBordLignes.setRange(0, 60)
        self.spinTableauBordLignes.setValue(52)
        self.spinTableauBordLignes.setStyleSheet("max-width: 70px;")
        label_lignes = QtWidgets.QLabel("Nombre de lignes visibles", self.tableau_de_bord)
        
        layout_lignes.addWidget(self.spinTableauBordLignes)
        layout_lignes.addWidget(label_lignes)
        
        self.curseurTableauBordLignes = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.tableau_de_bord)
        self.curseurTableauBordLignes.setRange(0, 60)
        self.curseurTableauBordLignes.setValue(52)
        self.curseurTableauBordLignes.setStyleSheet("margin-bottom: 40px; max-width: 400px;")
        
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
        layout_tableau_bord.addWidget(self.curseurTableauBordColonnes)
        layout_tableau_bord.addLayout(layout_lignes)
        layout_tableau_bord.addWidget(self.curseurTableauBordLignes)
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
        
        self.graphe = Graphe(rows, cols, parent=self.labels_grille)
        self.graphe.afficher_grille(self.labels_grille)
        
        for (i, j), drop_area in self.graphe.cellules_graphiques.items():
            drop_area.placer_produit.connect(self.on_placer_produit)
            drop_area.cellule_cliquee.connect(self.on_cellule_cliquee)
            self.cellules_grille[(i, j)] = drop_area
    
    def connecter_signaux(self):
        """Connecte les signaux internes"""
        # Synchronisation spin/slider
        self.spinTableauBordColonnes.valueChanged.connect(self.curseurTableauBordColonnes.setValue)
        self.curseurTableauBordColonnes.valueChanged.connect(self.spinTableauBordColonnes.setValue)
        self.spinTableauBordLignes.valueChanged.connect(self.curseurTableauBordLignes.setValue)
        self.curseurTableauBordLignes.valueChanged.connect(self.spinTableauBordLignes.setValue)
        
        # Émission des signaux vers le contrôleur
        self.spinTableauBordColonnes.valueChanged.connect(self.on_dimensions_changees)
        self.spinTableauBordLignes.valueChanged.connect(self.on_dimensions_changees)
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
        self.create_grille(rows, cols)
    
    def effacer_grille(self):
        """Efface tous les produits de la grille"""
        for cellule in self.cellules_grille.values():
            cellule.setText("")
            cellule.setStyleSheet("border: 1px solid rgba(0, 0, 0, 0.8); background-color: #00000000;")


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
