from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication
import sys

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
        self.partieGauche.setStyleSheet("background-color: #232323;")
        
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

        layoutArticles.addWidget(self.listeArticlesrecherche, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # Ajout du tableau de bord
        self.tableauDeBord = QtWidgets.QWidget(self.partieGauche)
        self.tableauDeBord.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.tableauDeBord.setMinimumHeight(100)

        layoutTableauBord = QtWidgets.QVBoxLayout(self.tableauDeBord)

        self.labelTableauBord = QtWidgets.QLabel("Réglages du magasin", self.tableauDeBord)
        self.curseurTableauBord = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self.tableauDeBord)
        self.spinTableauBord = QtWidgets.QSpinBox(self.tableauDeBord)
        self.spinTableauBord.setRange(0, 4)

        layoutTableauBord.addWidget(self.labelTableauBord)
        layoutTableauBord.addWidget(self.curseurTableauBord)
        layoutTableauBord.addWidget(self.spinTableauBord)

        # Ajout des widgets à la partie gauche
        layout.addWidget(self.listeArticles, stretch=4)
        layout.addWidget(self.tableauDeBord, stretch=1)
        self.layout.addWidget(self.partieGauche, stretch=1)

    def create_partieDroite(self):
        # Paramètres de la partie droite
        self.partieDroite = QtWidgets.QWidget(self)
        self.partieDroite.setStyleSheet("background-color: #232323;")
        
        layout = QtWidgets.QVBoxLayout(self.partieDroite)
        layout.stretch(1)

        
        self.label = QtWidgets.QLabel("Partie Droite", self.partieDroite)
        layout.addWidget(self.label)

        self.layout.addWidget(self.partieDroite, stretch=1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VueAdmin()
    window.show()
    sys.exit(app.exec())