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


        # chargelement des produits depuis le fichier CSV
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "..", "liste_produits.csv")

        try:
            loader = lp.csvLoader(csv_path)
        except FileNotFoundError as e:
            print(f"Erreur : fichier non trouvé à {csv_path} -> {e}")
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
        
        # Colonnes (SpinBox + Label) 
        layoutColonnes = QtWidgets.QHBoxLayout()
        self.spinTableauBordColonnes = QtWidgets.QSpinBox(self.tableauDeBord)
        self.spinTableauBordColonnes.setRange(0, 50)
        self.spinTableauBordColonnes.setStyleSheet("max-width: 70px;")
        labelColonnes = QtWidgets.QLabel("Nombre de colonnes visibles", self.tableauDeBord)

        layoutColonnes.addWidget(self.spinTableauBordColonnes)
        layoutColonnes.addWidget(labelColonnes)

        # Slider Colonnes
        self.curseurTableauBordColonnes = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.tableauDeBord)
        self.curseurTableauBordColonnes.setRange(0, 50)
        self.curseurTableauBordColonnes.setStyleSheet("margin-bottom: 40px; max-width: 400px;")

        # Lignes (SpinBox + Label)
        layoutLignes = QtWidgets.QHBoxLayout()
        self.spinTableauBordLignes = QtWidgets.QSpinBox(self.tableauDeBord)
        self.spinTableauBordLignes.setRange(0, 60)
        self.spinTableauBordLignes.setStyleSheet("max-width: 70px;")
        labelLignes = QtWidgets.QLabel("Nombre de lignes visibles", self.tableauDeBord)

        layoutLignes.addWidget(self.spinTableauBordLignes)
        layoutLignes.addWidget(labelLignes)

        # Slider Lignes 
        self.curseurTableauBordLignes = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.tableauDeBord)
        self.curseurTableauBordLignes.setRange(0, 60)
        self.curseurTableauBordLignes.setStyleSheet("margin-bottom: 40px; max-width: 400px;")

        self.spinTableauBordColonnes.setValue(35)
        self.spinTableauBordLignes.setValue(52)

        self.spinTableauBordColonnes.valueChanged.connect(self.curseurTableauBordColonnes.setValue)
        self.curseurTableauBordColonnes.valueChanged.connect(self.spinTableauBordColonnes.setValue)
        self.spinTableauBordLignes.valueChanged.connect(self.curseurTableauBordLignes.setValue)
        self.curseurTableauBordLignes.valueChanged.connect(self.spinTableauBordLignes.setValue)

        # Ajout d'un layout horizontal pour les boutons
        layoutBoutons = QtWidgets.QHBoxLayout()
        layoutBoutons.setContentsMargins(10, 10, 10, 10)

        # Ajout des boutons pour ouvrir, sauvegarder et effacer le projet.
        self.boutonOuvrir = QtWidgets.QPushButton("Ouvrir", self.tableauDeBord)
        self.boutonOuvrir.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.boutonOuvrir.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px; margin-bottom: 10px;")
        self.boutonOuvrir.setMaximumWidth(200)
        self.boutonOuvrir.setMaximumHeight(50)
        self.bouotonSauvegarder = QtWidgets.QPushButton("Sauvegarder", self.tableauDeBord)
        self.bouotonSauvegarder.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.bouotonSauvegarder.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px; margin-bottom: 10px;")
        self.bouotonSauvegarder.setMaximumWidth(200)
        self.bouotonSauvegarder.setMaximumHeight(50)
        self.boutonEffacer = QtWidgets.QPushButton("Effacer", self.tableauDeBord)
        self.boutonEffacer.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.boutonEffacer.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px; margin-bottom: 10px;")
        self.boutonEffacer.setMaximumWidth(200)
        self.boutonEffacer.setMaximumHeight(50)

        # Ajout des boutons au layout
        layoutBoutons.addWidget(self.boutonOuvrir)
        layoutBoutons.addWidget(self.bouotonSauvegarder)
        layoutBoutons.addWidget(self.boutonEffacer)


        layoutTableauBord.addWidget(self.labelTableauBord)
        layoutTableauBord.addLayout(layoutColonnes)
        layoutTableauBord.addWidget(self.curseurTableauBordColonnes)
        layoutTableauBord.addLayout(layoutLignes)
        layoutTableauBord.addWidget(self.curseurTableauBordLignes)
        layoutTableauBord.addLayout(layoutBoutons)



        # Ajout des widgets à la partie gauche
        layout.addWidget(self.listeArticles, stretch=2)
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
        self.nomMagasin.setMinimumWidth(400)
        self.nomMagasin.setMaximumWidth(400)
        self.nomMagasin.setStyleSheet("padding: 5px;")

        layoutHeader.addWidget(self.label)
        layoutHeader.addWidget(self.nomMagasin)

        # Zone superposée
        self.zoneSuperposee = QtWidgets.QWidget(self.partieDroite)
        self.zoneSuperposee.setContentsMargins(0, 0, 0, 0)
        self.zoneSuperposee.setFixedSize(760, 900)
        self.zoneSuperposee.setStyleSheet("background-color: transparent;")

        self.labelPlan = QtWidgets.QLabel(self.zoneSuperposee)
        self.labelPlan.setGeometry(0, 0, 760, 900)

        transform = QTransform().rotate(90)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin = os.path.join(script_dir, "..", "plan_magasin.jpg")

        plan = QPixmap(chemin)

        if plan.isNull():
            print(f"Erreur : l'image n'a pas pu être chargée depuis {chemin}")
            plan = QPixmap(760, 900)  # image vide par défaut

        plan = plan.transformed(transform)
        self.labelPlan.setPixmap(plan)
        self.labelPlan.setScaledContents(True)
        self.labelPlan.setMaximumSize(760, 900)
        self.labelPlan.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.labelPlan.setStyleSheet("background-color: transparent;")

        # Grille par-dessus
        self.labelsGrille = QtWidgets.QWidget(self.zoneSuperposee)
        self.labelsGrille.setStyleSheet("background-color: transparent;")

        displayed_width = self.labelPlan.width()
        displayed_height = self.labelPlan.height()
        self.labelsGrille.setGeometry(self.labelPlan.geometry())
        self.labelsGrille.resize(displayed_width, displayed_height)

        rows, cols = 52, 35
        cell_width = displayed_width / cols
        cell_height = displayed_height / rows

        for i in range(rows):
            for j in range(cols):
                cell = DropArea(self.labelsGrille)
                x = int(j * cell_width)
                y = int(i * cell_height)
                width = int(cell_width) if j < cols - 1 else (displayed_width - int(j * cell_width))
                height = int(cell_height) if i < rows - 1 else (displayed_height - int(i * cell_height))
                cell.setGeometry(x, y, width, height)
                cell.setStyleSheet("border: 1px solid rgba(0, 0, 0, 0.3); background-color: #00000000;")

        layout.addWidget(header, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.zoneSuperposee, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.partieDroite, stretch=1)





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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: transparent;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        produit = event.mimeData().text()
        print(f"[DROP] Produit déposé : {produit}")
        self.setText(produit)
        self.setStyleSheet("background-color: rgba(100, 100, 100, 0.6); color: white; border-radius: 4px;")
        event.acceptProposedAction()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VueAdmin()
    window.show()
    sys.exit(app.exec())