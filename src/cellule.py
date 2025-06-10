from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
import os

class Cellule:
    "représente une cellule (sommet du graphe)"
    def __init__(self, contenu, est_rayon, voisins):
        self.contenu = contenu if contenu else []
        self.est_rayon = est_rayon
        self.voisins = voisins if voisins else []
        self.position = None

    def set_position(self, ligne, colonne):
        """Définit la position de la cellule"""
        self.position = (ligne, colonne)

    def est_voisin(self, autre_cellule):
        """Vérifie si deux cellules sont voisines"""
        return autre_cellule in self.voisins