from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication
import sys
import os

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

        self.articlesBox = QtWidgets.QWidget(self.listeArticles)
        self.articlesBox.setStyleSheet("border: 5px solid #232323;")

        layoutarticlesBox = QtWidgets.QHBoxLayout(self.articlesBox)

        layoutArticles.addWidget(self.listeArticlesrecherche, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft, stretch=1)
        layoutArticles.addWidget(self.articlesBox, stretch=12)

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

        layout.addWidget(header, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.partieDroite, stretch=1)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VueAdmin()
    window.show()
    sys.exit(app.exec())