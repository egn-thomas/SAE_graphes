from cellule import Cellule
from PyQt6.QtWidgets import QWidget, QLabel
from droparea import DropArea

class Graphe:
    """Représente le graphe du magasin"""
    def __init__(self, nb_lignes: int, nb_colonnes: int, parent: QWidget = None):
        self.graphe = {}
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.parent = parent
        self.cellules_graphiques = {}
        self.initialiser_graphe()
    
    def initialiser_graphe(self):
        """initialise le graphe avec des Cellules"""
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                # Créer la cellule logique
                cellule = Cellule(contenu=[], est_rayon=False, voisins=[])
                cellule.set_position(i, j)
                self.graphe[(i, j)] = cellule
                
                # Créer la cellule graphique (DropArea)
                drop_area = DropArea(self.parent)
                drop_area.ligne = i
                drop_area.colonne = j
                drop_area.setStyleSheet("""
                    background-color: transparent;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                """)
                self.cellules_graphiques[(i, j)] = drop_area
        
        self.connecter_cellules()

    def afficher_grille(self, container_widget, rows, cols):
        """Affiche la grille graphique sur le widget conteneur"""
        # Dimensions du conteneur
        displayed_width = container_widget.width()
        displayed_height = container_widget.height()
        cell_width = displayed_width / cols
        cell_height = displayed_height / rows
        
        # Positionner chaque cellule
        for (i, j), drop_area in self.cellules_graphiques.items():
            x = int(j * cell_width)
            y = int(i * cell_height)
            width = int(cell_width) if j < cols - 1 else (displayed_width - int(j * cell_width))
            height = int(cell_height) if i < rows - 1 else (displayed_height - int(i * cell_height))
            
            drop_area.setGeometry(x, y, width, height)
            drop_area.setStyleSheet("""
                background-color: transparent;
                border: 1px solid rgba(0, 0, 0, 0.3);
            """)
            drop_area.show()

    def connecter_cellules(self):
        """Créé les connexions entre les cellules"""
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        
        for (l, c) in self.graphe:
            cellule = self.graphe[(l, c)]
            for dl, dc in directions:
                pos_voisin = (l+dl, c+dc)
                if pos_voisin in self.graphe:
                    cellule.voisins.append(self.graphe[pos_voisin])
    
    def afficher_graphe(self):
        """affiche le graphe"""
        for (l, c) in self.graphe:
            cellule = self.graphe[(l, c)]
            voisins = [(l+dl, c+dc) for dl, dc in [(0,1), (0,-1), (1,0), (-1,0)] 
                    if (l+dl, c+dc) in self.graphe]
            print(f"Cellule ({l},{c}):")
            print(f"  Contenu: {cellule.contenu}")
            print(f"  Est rayon: {cellule.est_rayon}")
            print(f"  Voisins: {voisins}\n")