from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QApplication
import sys
import os
import listeProduit as lp





class VueAdmin(QtWidgets.QWidget):
    def __init__(self):
        super(VueAdmin, self).__init__()

        self.setWindowTitle("Créateur de magazin Administrateur")
        self.setGeometry(200, 200, 1600, 1200)

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


        # Charger les données
        try:
            path = "../liste_produits.csv"
            loader = lp.csvLoader(path)
        except FileNotFoundError:
            try:
                path = "..\liste_produits.csv"
                loader = lp.csvLoader(path)
            except FileNotFoundError:
                print("Erreur : aucun fichier produits trouvé.")
                loader = None


        produits = loader.extract_all()

        categories = produits[0]
        liste_produits = [dict(zip(categories, row)) for row in produits[1:]]

        self.produits_par_categorie = {cat: [] for cat in categories}

        for produit in liste_produits:
            for cat in categories:
                valeur = produit[cat]
                if valeur:
                    self.produits_par_categorie[cat].append(valeur)

        # Ajouter un bouton par catégorie
        for categorie in categories:
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

        # --- Colonnes (SpinBox + Label) ---
        layoutColonnes = QtWidgets.QHBoxLayout()
        self.spinTableauBordColonnes = QtWidgets.QSpinBox(self.tableauDeBord)
        self.spinTableauBordColonnes.setRange(0, 4)
        self.spinTableauBordColonnes.setStyleSheet("max-width: 50px;")
        labelColonnes = QtWidgets.QLabel("Nombre de colonnes visibles", self.tableauDeBord)

        layoutColonnes.addWidget(self.spinTableauBordColonnes)
        layoutColonnes.addWidget(labelColonnes)

        # --- Slider Colonnes ---
        self.curseurTableauBordColonnes = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.tableauDeBord)
        self.curseurTableauBordColonnes.setRange(0, 15)
        self.curseurTableauBordColonnes.setStyleSheet("margin-bottom: 40px; max-width: 200px;")

        # --- Lignes (SpinBox + Label) ---
        layoutLignes = QtWidgets.QHBoxLayout()
        self.spinTableauBordLignes = QtWidgets.QSpinBox(self.tableauDeBord)
        self.spinTableauBordLignes.setRange(0, 4)
        self.spinTableauBordLignes.setStyleSheet("max-width: 50px;")
        labelLignes = QtWidgets.QLabel("Nombre de lignes visibles", self.tableauDeBord)

        layoutLignes.addWidget(self.spinTableauBordLignes)
        layoutLignes.addWidget(labelLignes)

        # --- Slider Lignes ---
        self.curseurTableauBordLignes = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.tableauDeBord)
        self.curseurTableauBordLignes.setRange(0, 15)
        self.curseurTableauBordLignes.setStyleSheet("margin-bottom: 40px; max-width: 200px;")

        # --- Ajout au layout principal ---
        layoutTableauBord.addWidget(self.labelTableauBord)
        layoutTableauBord.addLayout(layoutColonnes)
        layoutTableauBord.addWidget(self.curseurTableauBordColonnes)
        layoutTableauBord.addLayout(layoutLignes)
        layoutTableauBord.addWidget(self.curseurTableauBordLignes)



        # Ajout des widgets à la partie gauche
        layout.addWidget(self.listeArticles, stretch=4)
        layout.addWidget(self.tableauDeBord, stretch=1)
        
        self.layout.addWidget(self.partieGauche, stretch=1)





    def create_partieDroite(self):
        # Paramètres de la partie droite
        self.partieDroite = QtWidgets.QWidget(self)
        self.partieDroite.setStyleSheet("background-color: #232323;")
        
        layout = QtWidgets.QVBoxLayout(self.partieDroite)

        # Header avec label et champ de texte
        header = QtWidgets.QWidget(self.partieDroite)
        layoutHeader = QtWidgets.QHBoxLayout(header)
        layoutHeader.setContentsMargins(10, 10, 10, 10)
        layoutHeader.setSpacing(10)
        
        self.label = QtWidgets.QLabel("Votre magasin :", self.partieDroite)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.label.setStyleSheet("color: white; font-size: 16px;")

        self.nomMagasin = QtWidgets.QLineEdit(self.partieDroite)
        self.nomMagasin.setPlaceholderText("Nom du magasin")
        self.nomMagasin.setMinimumWidth(400)
        self.nomMagasin.setMaximumWidth(400)
        self.nomMagasin.setStyleSheet("padding: 5px;")

        layoutHeader.addWidget(self.label)
        layoutHeader.addWidget(self.nomMagasin)

        self.labelPlan = DropArea(self.partieDroite)
        transform = QTransform().rotate(90)

        try:
            path = "../plan_magasin.jpg"
            plan = QPixmap(path)
        except FileNotFoundError:
            try:
                path = "..\plan_magasin.jpg"
                plan = QPixmap(path)
                
            except FileNotFoundError:
                print("Erreur : aucun plan de magazin trouvé.")
                loader = None

        plan = plan.transformed(transform)
        self.labelPlan.setPixmap(plan)
        self.labelPlan.setScaledContents(True)
        self.labelPlan.setMaximumSize(760, 900)
        self.labelPlan.setStyleSheet("margin-left: 160px; margin-bottom: 100px")

    

        layout.addWidget(header, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.labelPlan)

        self.layout.addWidget(self.partieDroite, stretch=1)





    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()





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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setPixmap(QPixmap("../plan_magasin.jpg").transformed(QTransform().rotate(90)))
        self.setScaledContents(True)
        self.setMaximumSize(760, 900)
        self.setStyleSheet("margin-left: 160px; margin-bottom: 100px")

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        produit = event.mimeData().text()
        print(f"[DROP] Produit déposé : {produit}")

        # Option visuelle : afficher un petit label sur la zone
        label = QtWidgets.QLabel(produit, self)
        label.move(event.position().toPoint())  # Qt 6.0+
        label.setStyleSheet("background-color: #555; color: white; padding: 2px; border-radius: 2px;")
        label.adjustSize()
        label.show()

        event.acceptProposedAction()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VueAdmin()
    window.show()
    sys.exit(app.exec())