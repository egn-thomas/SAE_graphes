from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
import os

class Cellule:
    """Représente une cellule logique (sommet du graphe)"""
    def __init__(self, contenu, est_rayon):
        self.contenu = contenu if contenu else []
        self.est_rayon = bool(est_rayon)
        self.voisins = []
        self.position = None

    def ajouter_contenu(self, element):
        """Ajoute un élément au contenu"""
        if element not in self.contenu:
            self.contenu.append(element)
            return True
        return False

    def supprimer_contenu(self, element):
        """Supprime un élément du contenu"""
        if element in self.contenu:
            self.contenu.remove(element)
            return True
        return False
    
    def set_position(self, ligne, colonne):
        """Définit la position de la cellule"""
        self.position = (ligne, colonne)

    def get_position(self):
        return self.position

    def ajouter_voisin(self, cellule):
        """Ajoute une cellule voisine"""
        if cellule not in self.voisins:
            self.voisins.append(cellule)
            return True
        return False

    def est_voisin(self, autre_cellule):
        """Vérifie si deux cellules sont voisines"""
        return autre_cellule in self.voisins
    
    def marquer_comme_entree(self):
        """Marque la cellule comme entrée du magasin"""
        self.setStyleSheet("background-color: #90EE90; border: 2px solid #006400;")
    
    def reinitialiser(self):
        """Remet la cellule à son état initial (sauf si c'est un produit ou l'entrée)"""
        self.est_chemin = False
        self.numero_ordre = None
        
        if self.est_produit:
            # Remettre la couleur du produit
            self.setStyleSheet("background-color: #FFD700; border: 2px solid #FFA500;")
        elif self.x == 0 and self.y == 0:  # Entrée
            self.marquer_comme_entree()
        else:
            # Remettre la couleur originale
            self.setStyleSheet(f"background-color: {self.couleur_originale}; border: 1px solid #cccccc;")