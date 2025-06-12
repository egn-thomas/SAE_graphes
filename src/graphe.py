from cellule import Cellule
from droparea import DropArea
from PyQt6.QtWidgets import QWidget

class Graphe:
    """Représente le graphe du magasin et gère son affichage"""
    def __init__(self, nb_lignes: int, nb_colonnes: int, cases_colorees, parent=None):
        self.graphe = {}
        self.cellules_graphiques = {}
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.cases_colorees = cases_colorees
        self.parent = parent
        self.initialiser_graphe()

    def initialiser_graphe(self):
        """Initialise la structure logique et graphique"""
        
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                if (i, j) in self.cases_colorees:
                    est_rayon = True
                else:
                    est_rayon = False
                cellule = Cellule(None, est_rayon)
                cellule.set_position(i, j)
                self.graphe[(i, j)] = cellule

        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                self._creer_cellule_graphique(i, j)

        self.connecter_cellules()

    def _creer_cellule_graphique(self, i, j):
        """Crée une cellule graphique"""
        if (i, j) in self.cases_colorees:
            est_rayon = True
        else:
            est_rayon = False
        drop_area = DropArea(self.parent, est_rayon)
        drop_area.ligne = i
        drop_area.colonne = j
        cellule_logique = self.graphe[(i, j)]
        drop_area.lier_cellule(cellule_logique)
        self.cellules_graphiques[(i, j)] = drop_area

    def connecter_cellules(self):
        """Établit les connexions entre cellules"""
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        for (l, c) in self.graphe:
            cellule = self.graphe[(l, c)]
            for dl, dc in directions:
                pos_voisin = (l+dl, c+dc)
                if pos_voisin in self.graphe:
                    cellule.ajouter_voisin(self.graphe[pos_voisin])

    def ajouter_contenu(self, ligne, colonne, element):
        """Ajoute un contenu à une cellule"""
        if (ligne, colonne) in self.graphe:
            return self.graphe[(ligne, colonne)].ajouter_contenu(element)
        return False

    def get_cellule(self, ligne, colonne):
        """Récupère une cellule"""
        return self.graphe.get((ligne, colonne))

    def afficher_grille(self, container_widget):
        """Affiche la grille graphiquement"""
        if not self.parent:
            return

        width = container_widget.width()
        height = container_widget.height()
        cell_width = width / self.nb_colonnes
        cell_height = height / self.nb_lignes
        
        for (i, j), drop_area in self.cellules_graphiques.items():
            x = int(j * cell_width)
            y = int(i * cell_height)
            width_cell = int(cell_width) if j < self.nb_colonnes - 1 else (width - int(j * cell_width))
            height_cell = int(cell_height) if i < self.nb_lignes - 1 else (height - int(i * cell_height))
            
            drop_area.setGeometry(x, y, width_cell, height_cell)
            drop_area.show()