from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QApplication
import sys
import os
import listeProduit as lp
from magasin import Magasin


class VueAdmin(QtWidgets.QWidget):
    def __init__(self, nom_magasin="Mon Magasin", nb_lignes=52, nb_colonnes=35, csv_path=None, plan_path=None):
        super(VueAdmin, self).__init__()

        self.setWindowTitle("Créateur de magasin Administrateur")
        self.setGeometry(200, 200, 1600, 1200)

        # Initialisation du magasin
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Chemins par défaut si non spécifiés
        if csv_path is None:
            csv_path = os.path.join(script_dir, "..", "liste_produits.csv")
        if plan_path is None:
            plan_path = os.path.join(script_dir, "..", "plan_magasin.jpg")

        # Chargement des produits
        try:
            loader = lp.csvLoader(csv_path)
            produits = loader.extract_all()
            categories = produits[0]
            liste_produits = [dict(zip(categories, row)) for row in produits[1:]]
        except FileNotFoundError as e:
            print(f"Erreur : fichier non trouvé à {csv_path} -> {e}")
            categories = []
            liste_produits = []

        # Création de l'instance Magasin
        self.magasin = Magasin(
            nom=nom_magasin,
            path_plan_magasin=plan_path,
            liste_produits=liste_produits,
            nb_colonnes=nb_colonnes,
            nb_lignes=nb_lignes
        )

        # Organisation des produits par catégorie
        self.produits_par_categorie = {cat: [] for cat in categories}
        for produit in liste_produits:
            for cat in categories:
                valeur = produit[cat]
                if valeur:
                    self.produits_par_categorie[cat].append(valeur)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.create_partieGauche()
        self.create_partieDroite()

    def create_partieGauche(self):
        # Paramètres de la partie gauche
        self.partieGauche = QtWidgets.QWidget(self)
        self.partieGauche.setMinimumWidth(200)
        self.partieGauche.setStyleSheet("background-color: #232323; font-size: 16px; color: white;")
        
        layout = QtWidgets.QVBoxLayout(self.partieGauche)

        # Création de la liste des articles
        self.listeArticles = QtWidgets.QWidget(self.partieGauche)
        self.listeArticles.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.listeArticles.setMinimumHeight(100)

        layoutArticles = QtWidgets.QVBoxLayout(self.listeArticles)

        self.listeArticlesrecherche = QtWidgets.QLineEdit(self.listeArticles)
        self.listeArticlesrecherche.setPlaceholderText("Rechercher un article...")
        self.listeArticlesrecherche.setMinimumWidth(400)
        self.listeArticlesrecherche.setStyleSheet("padding: 5px; margin-left: 20px; margin-top: 20px;")

        # Créer articlesBox et son layout
        self.articlesBox = QtWidgets.QWidget(self.listeArticles)
        self.layoutarticlesBox = QtWidgets.QVBoxLayout(self.articlesBox)
        self.layoutarticlesBox.setContentsMargins(20, 20, 20, 140)
        self.layoutarticlesBox.setSpacing(10)

        # Ajouter un bouton par catégorie
        for categorie in self.produits_par_categorie.keys():
            btn = QtWidgets.QPushButton(categorie, self.articlesBox)
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(55)
            btn.setMinimumWidth(150)
            btn.clicked.connect(lambda checked, cat=categorie: self.afficher_produits_de_categorie(cat))
            btn.setStyleSheet("background-color: #232323; border-radius: 5px; color: white; padding: 10px; margin-bottom: 10px;")
            self.layoutarticlesBox.addWidget(btn, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        scroll = QtWidgets.QScrollArea(self.listeArticles)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        scroll.setWidget(self.articlesBox)

        layoutArticles.addWidget(self.listeArticlesrecherche, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft, stretch=1)
        layoutArticles.addWidget(scroll, stretch=12)

        # Ajout du tableau de bord
        self.tableauDeBord = QtWidgets.QWidget(self.partieGauche)
        self.tableauDeBord.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.tableauDeBord.setMinimumHeight(100)
        self.tableauDeBord.setContentsMargins(40, 0, 0, 0)

        layoutTableauBord = QtWidgets.QVBoxLayout(self.tableauDeBord)

        self.labelTableauBord = QtWidgets.QLabel("Réglages du magasin", self.tableauDeBord)
        
        self.spinTableauBord = QtWidgets.QSpinBox(self.tableauDeBord)
        self.spinTableauBord.setRange(0, 4)
        self.spinTableauBord.setStyleSheet("max-width: 50px;")
        
        self.curseurTableauBord = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.tableauDeBord)
        self.curseurTableauBord.setRange(0, 4)
        self.curseurTableauBord.setStyleSheet("margin-bottom: 40px; max-width: 200px;")

        layoutTableauBord.addWidget(self.labelTableauBord)
        layoutTableauBord.addWidget(self.spinTableauBord)
        layoutTableauBord.addWidget(self.curseurTableauBord)

        # Ajout des widgets à la partie gauche
        layout.addWidget(self.listeArticles, stretch=4)
        layout.addWidget(self.tableauDeBord, stretch=1)
        
        self.layout.addWidget(self.partieGauche, stretch=1)

    def create_partieDroite(self):
        self.partieDroite = QtWidgets.QWidget(self)
        self.partieDroite.setStyleSheet("background-color: #232323;")
        layout = QtWidgets.QVBoxLayout(self.partieDroite)

        # Header
        header = QtWidgets.QWidget(self.partieDroite)
        layoutHeader = QtWidgets.QHBoxLayout(header)
        layoutHeader.setContentsMargins(10, 10, 10, 10)
        layoutHeader.setSpacing(10)

        self.label = QtWidgets.QLabel("Votre magasin :", self.partieDroite)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.label.setStyleSheet("color: white; font-size: 16px;")

        self.nomMagasin = QtWidgets.QLineEdit(self.partieDroite)
        self.nomMagasin.setPlaceholderText("Nom du magasin")
        self.nomMagasin.setText(self.magasin.nom)
        self.nomMagasin.setMinimumWidth(400)
        self.nomMagasin.setMaximumWidth(400)
        self.nomMagasin.setStyleSheet("padding: 5px;")
        self.nomMagasin.textChanged.connect(self.changer_nom_magasin)

        layoutHeader.addWidget(self.label)
        layoutHeader.addWidget(self.nomMagasin)

        # Zone superposée
        self.zoneSuperposee = QtWidgets.QWidget(self.partieDroite)
        self.zoneSuperposee.setContentsMargins(0, 0, 0, 0)
        self.zoneSuperposee.setFixedSize(760, 900)
        self.zoneSuperposee.setStyleSheet("background-color: transparent;")

        self.create_plan_et_grille()

        layout.addWidget(header, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.zoneSuperposee, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.partieDroite, stretch=1)

    def create_plan_et_grille(self):
        # Chargement et affichage du plan
        self.labelPlan = QtWidgets.QLabel(self.zoneSuperposee)
        self.labelPlan.setGeometry(0, 0, 760, 900)

        transform = QTransform().rotate(90)
        plan = QPixmap(self.magasin.path_plan_magasin)

        if plan.isNull():
            print(f"Erreur : l'image n'a pas pu être chargée depuis {self.magasin.path_plan_magasin}")
            plan = QPixmap(760, 900)  # image vide par défaut

        plan = plan.transformed(transform)
        self.labelPlan.setPixmap(plan)
        self.labelPlan.setScaledContents(True)
        self.labelPlan.setMaximumSize(760, 900)
        self.labelPlan.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.labelPlan.setStyleSheet("background-color: transparent;")

        # Initialiser le plan dans l'objet magasin
        self.magasin.initialiser_plan(plan)

        # Créer la grille
        self.create_grille()

    def create_grille(self):
        # Supprimer l'ancienne grille si elle existe
        if hasattr(self, 'labelsGrille'):
            self.labelsGrille.deleteLater()

        # Grille par-dessus
        self.labelsGrille = QtWidgets.QWidget(self.zoneSuperposee)
        self.labelsGrille.setStyleSheet("background-color: transparent;")

        displayed_width = self.labelPlan.width()
        displayed_height = self.labelPlan.height()
        self.labelsGrille.setGeometry(self.labelPlan.geometry())
        self.labelsGrille.resize(displayed_width, displayed_height)

        rows, cols = self.magasin.nb_lignes, self.magasin.nb_colonnes
        cell_width = displayed_width / cols
        cell_height = displayed_height / rows

        for i in range(rows):
            for j in range(cols):
                cell = DropArea(self.labelsGrille, self.magasin, self)  # Passer self comme parent VueAdmin
                coord = f"{chr(65 + j)}{i + 1}"  # A1, B2, etc.
                cell.coord = coord
                cell.ligne = i
                cell.colonne = j
                
                # Affecter la cellule au magasin
                self.magasin.affecter_cellule(coord, cell)
                
                x = int(j * cell_width)
                y = int(i * cell_height)
                width = int(cell_width) if j < cols - 1 else (displayed_width - int(j * cell_width))
                height = int(cell_height) if i < rows - 1 else (displayed_height - int(i * cell_height))
                cell.setGeometry(x, y, width, height)
                cell.setStyleSheet("border: 1px solid rgba(0, 0, 0, 0.3); background-color: #00000000;")

    def mettre_a_jour_affichage_produits(self):
        """Met à jour l'affichage de la liste des produits avec leurs coordonnées"""
        # Vider le layout existant
        while self.layoutProduits.count():
            child = self.layoutProduits.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Récupérer les produits avec coordonnées
        produits_coords = self.magasin.coord_produits.copy()
        
        if produits_coords:
            # Trier par coordonnées pour un affichage ordonné
            for coord in sorted(produits_coords.keys()):
                produit = produits_coords[coord]
                label = QtWidgets.QLabel(f"{coord}: {produit}")
                label.setStyleSheet("""
                    color: white; 
                    background-color: #333; 
                    padding: 3px 6px; 
                    margin: 1px; 
                    border-radius: 3px;
                    font-size: 12px;
                """)
                label.setWordWrap(True)
                self.layoutProduits.addWidget(label)
        else:
            label_vide = QtWidgets.QLabel("Aucun produit placé")
            label_vide.setStyleSheet("color: #888; font-style: italic; padding: 10px;")
            self.layoutProduits.addWidget(label_vide)
        
        # Forcer la mise à jour de l'affichage
        self.contenuProduits.adjustSize()
        self.affichageProduits.update()

    def sauvegarder_automatique(self):
        """Sauvegarde automatique du magasin"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin = os.path.join(script_dir, "..", f"{self.magasin.nom.replace(' ', '_')}_config.json")
        try:
            self.magasin.sauvegarder(chemin)
        except Exception as e:
            print(f"[ERROR] Erreur lors de la sauvegarde automatique : {e}")

    def changer_nom_magasin(self, text):
        self.magasin.nom = text
        self.sauvegarder_automatique()

    def recuperer_produits_avec_coordonnees(self):
        produits_coords = self.magasin.coord_produits.copy()
        
        # Afficher dans la console
        print("\n--- LISTE DES PRODUITS AVEC COORDONNÉES ---")
        if produits_coords:
            for coord in sorted(produits_coords.keys()):
                produit = produits_coords[coord]
                print(f"Cellule {coord}: {produit}")
        else:
            print("Aucun produit placé dans le magasin")
        
        return produits_coords

    def afficher_produits_de_categorie(self, categorie):
        print(f"[DEBUG] Categorie cliquée : {categorie}")
        self.clear_layout(self.layoutarticlesBox)

        # ← Bouton de retour
        btn_retour = QtWidgets.QPushButton("← Retour", self.articlesBox)
        btn_retour.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_retour.setFixedHeight(40)
        btn_retour.setMaximumWidth(150)
        btn_retour.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px; margin-bottom: 10px;")
        btn_retour.clicked.connect(self.afficher_categories)
        self.layoutarticlesBox.addWidget(btn_retour)

        produits = self.produits_par_categorie.get(categorie, [])
        print(f"[DEBUG] Produits : {produits}")

        for produit in produits:
            label = DraggableLabel(produit, self.articlesBox)
            label.setStyleSheet("color: white; background-color: #333; padding: 5px; border-radius: 3px;")
            label.setMinimumHeight(40)
            label.setMaximumWidth(300)
            self.layoutarticlesBox.addWidget(label)

        self.articlesBox.adjustSize()
        self.articlesBox.update()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def afficher_categories(self):
        self.clear_layout(self.layoutarticlesBox)

        for categorie in self.produits_par_categorie.keys():
            btn = QtWidgets.QPushButton(categorie, self.articlesBox)
            btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(55)
            btn.setMinimumWidth(150)
            btn.clicked.connect(lambda checked, cat=categorie: self.afficher_produits_de_categorie(cat))
            btn.setStyleSheet("background-color: #232323; border-radius: 5px; color: white; padding: 10px; margin-bottom: 10px;")
            self.layoutarticlesBox.addWidget(btn, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)


class DraggableLabel(QtWidgets.QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
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
            drag.setHotSpot(event.pos())

            drag.exec(QtCore.Qt.DropAction.MoveAction)


class DropArea(QtWidgets.QLabel):
    def __init__(self, parent=None, magasin=None, vue_admin=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: transparent;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Référence vers l'objet magasin et la vue admin
        self.magasin = magasin
        self.vue_admin = vue_admin
        
        # Initialiser les attributs nécessaires pour la popup
        self.popup_actuelle = None
        self.coord = ""  # Coordonnée de la cellule (ex: "A1")
        self.ligne = 0
        self.colonne = 0

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        produit = event.mimeData().text()
        print(f"[DROP] Produit déposé : {produit} sur {self.coord}")
        self.setText(produit)
        self.setStyleSheet("background-color: rgba(100, 100, 100, 0.6); color: white; border-radius: 4px;")
        
        # Enregistrer le produit dans le magasin
        if self.magasin:
            self.magasin.enregistrer_produit(self.coord, produit)
            if self.coord not in self.magasin.cases_rayon:
                self.magasin.cases_rayon.add(self.coord)
        
        # Afficher tous les produits dans le terminal
        print("\n--- LISTE DES PRODUITS AVEC COORDONNÉES ---")
        produits_coords = self.magasin.coord_produits.copy()
        if produits_coords:
            for coord in sorted(produits_coords.keys()):
                produit = produits_coords[coord]
                print(f"{coord}: {produit}")
        else:
            print("Aucun produit placé dans le magasin")

        # Sauvegarde automatique
        if self.vue_admin:
            self.vue_admin.sauvegarder_automatique()

        event.acceptProposedAction()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.creer_ou_fermer_popup()

    def creer_ou_fermer_popup(self):
        # Si une vignette est déjà ouverte sur cette cellule, on la ferme
        if self.popup_actuelle:
            self.popup_actuelle.hide()
            self.popup_actuelle.deleteLater()
            self.popup_actuelle = None
            return

        # Récupérer les produits de la cellule depuis le magasin
        produits = None
        if self.magasin:
            produits = self.magasin.coord_produits.get(self.coord, [])

        if not produits:
            return

        # Créer une nouvelle vignette
        vignette = QtWidgets.QWidget(self.parent())
        vignette.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Tool)
        vignette.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating)
        vignette.setStyleSheet("""
            QWidget {
                background-color: #404040;
                border: 2px solid #666;
                border-radius: 8px;
                color: white;
            }
            QLabel {
                color: white;
                padding: 5px;
                margin: 3px;
                background-color: #333;
                border-radius: 3px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(vignette)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Ajouter le titre avec les coordonnées
        label_coord = QtWidgets.QLabel(f"Cellule: {self.coord}")
        label_coord.setStyleSheet("font-weight: bold; background-color: transparent;")
        layout.addWidget(label_coord)

        # Ajouter chaque produit dans une case distincte
        for produit in produits:
            label_produit = QtWidgets.QLabel(produit)
            label_produit.setWordWrap(True)
            layout.addWidget(label_produit)

        # Calculer la position de la vignette
        pos_cellule = self.pos()
        pos_parent = self.parent().mapToGlobal(QtCore.QPoint(0, 0))
        
        vignette_x = pos_parent.x() + pos_cellule.x() + self.width() + 5
        vignette_y = pos_parent.y() + pos_cellule.y()
        
        # Ajuster la taille de la vignette
        vignette.adjustSize()
        vignette.setMinimumWidth(150)
        vignette.setMaximumWidth(250)
        
        # Vérifier que la vignette ne sorte pas de l'écran
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        if vignette_x + vignette.width() > screen_geometry.width():
            vignette_x = pos_parent.x() + pos_cellule.x() - vignette.width() - 5
        
        vignette.move(vignette_x, vignette_y)
        vignette.show()

        # Mémoriser la vignette
        self.popup_actuelle = vignette


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Exemple d'utilisation avec différents paramètres
    window = VueAdmin(
        nom_magasin="Projet 1",
        nb_lignes=52,
        nb_colonnes=35,
        # csv_path="chemin/vers/produits.csv",  # Optionnel
        # plan_path="chemin/vers/plan.jpg"      # Optionnel
    )
    
    window.show()
    sys.exit(app.exec())