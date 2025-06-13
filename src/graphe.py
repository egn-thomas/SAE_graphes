from cellule import Cellule
from droparea import DropArea
from PyQt6.QtWidgets import QWidget
from typing import List, Tuple, Optional
import heapq
from PyQt6.QtGui import QColor

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


class AlgorithmeDijkstra:
    """Implémentation de l'algorithme de Dijkstra pour le pathfinding"""
    
    @staticmethod
    def trouver_couloir_le_plus_proche(grille: List[List[bool]], position_rayon: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Trouve la case couloir la plus proche d'une position dans un rayon
        
        Args:
            grille: Matrice booléenne (True = couloir, False = rayon)
            position_rayon: Position dans le rayon (x, y)
            
        Returns:
            Coordonnées du couloir le plus proche ou None si aucun trouvé
        """
        if not grille or not grille[0]:
            return None
        
        hauteur, largeur = len(grille), len(grille[0])
        x_rayon, y_rayon = position_rayon
        
        # BFS pour trouver le couloir le plus proche
        queue = [(x_rayon, y_rayon, 0)]  # (x, y, distance)
        visites = {(x_rayon, y_rayon)}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        while queue:
            x, y, distance = queue.pop(0)
            
            # Si on trouve un couloir, c'est le plus proche
            if 0 <= x < largeur and 0 <= y < hauteur and grille[y][x]:
                return (x, y)
            
            # Explorer les voisins
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < largeur and 0 <= ny < hauteur and 
                    (nx, ny) not in visites):
                    visites.add((nx, ny))
                    queue.append((nx, ny, distance + 1))
        
        return None
    
    @staticmethod
    def dijkstra(grille: List[List[bool]], depart: Tuple[int, int], arrivee: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Trouve le chemin le plus court entre deux points
        
        Args:
            grille: Matrice booléenne (True = couloir praticable, False = rayon)
            depart: Coordonnées de départ (x, y)
            arrivee: Coordonnées d'arrivée (x, y)
            
        Returns:
            Liste des coordonnées du chemin optimal
        """
        if not grille or not grille[0]:
            return []
        
        hauteur, largeur = len(grille), len(grille[0])
        
        # Vérifier que les points sont valides
        if (not (0 <= depart[1] < hauteur and 0 <= depart[0] < largeur) or
            not (0 <= arrivee[1] < hauteur and 0 <= arrivee[0] < largeur)):
            return []
        
        # Si le point de départ ou d'arrivée n'est pas dans un couloir,
        # trouver le couloir le plus proche
        depart_reel = depart
        arrivee_reelle = arrivee
        
        if not grille[depart[1]][depart[0]]:
            depart_reel = AlgorithmeDijkstra.trouver_couloir_le_plus_proche(grille, depart)
            if not depart_reel:
                return []
        
        if not grille[arrivee[1]][arrivee[0]]:
            arrivee_reelle = AlgorithmeDijkstra.trouver_couloir_le_plus_proche(grille, arrivee)
            if not arrivee_reelle:
                return []
        
        # Directions possibles (haut, bas, gauche, droite)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # File de priorité pour Dijkstra
        pq = [(0, depart_reel)]
        distances = {depart_reel: 0}
        precedents = {}
        visites = set()
        
        while pq:
            distance_actuelle, (x, y) = heapq.heappop(pq)
            
            if (x, y) in visites:
                continue
                
            visites.add((x, y))
            
            # Si on a atteint l'arrivée
            if (x, y) == arrivee_reelle:
                break
            
            # Explorer les voisins
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Vérifier les limites et si c'est un couloir
                if (0 <= nx < largeur and 0 <= ny < hauteur and 
                    grille[ny][nx] and (nx, ny) not in visites):
                    
                    nouvelle_distance = distance_actuelle + 1
                    
                    if (nx, ny) not in distances or nouvelle_distance < distances[(nx, ny)]:
                        distances[(nx, ny)] = nouvelle_distance
                        precedents[(nx, ny)] = (x, y)
                        heapq.heappush(pq, (nouvelle_distance, (nx, ny)))
        
        # Reconstruire le chemin
        if arrivee_reelle not in precedents and arrivee_reelle != depart_reel:
            return []  # Pas de chemin trouvé
        
        chemin = []
        actuel = arrivee_reelle
        
        while actuel is not None:
            chemin.append(actuel)
            actuel = precedents.get(actuel)
        
        return chemin[::-1]  # Inverser pour avoir le chemin du départ à l'arrivée

class OptimiseurTSP:
    """Optimiseur simple pour le problème du voyageur de commerce (TSP)"""
    
    @staticmethod
    def calculer_distance_manhattan(point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
        """Calcule la distance de Manhattan entre deux points"""
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
    
    @staticmethod
    def optimiser_ordre_visite(depart: Tuple[int, int], destinations: List[Tuple[str, Tuple[int, int]]]) -> List[str]:
        """
        Optimise l'ordre de visite des destinations (algorithme glouton simple)
        
        Args:
            depart: Position de départ
            destinations: Liste de (nom_produit, position)
            
        Returns:
            Liste des noms de produits dans l'ordre optimal de visite
        """
        if not destinations:
            return []
        
        non_visites = destinations.copy()
        ordre_visite = []
        position_actuelle = depart
        
        while non_visites:
            # Trouver la destination la plus proche
            plus_proche = min(non_visites, 
                            key=lambda dest: OptimiseurTSP.calculer_distance_manhattan(position_actuelle, dest[1]))
            
            ordre_visite.append(plus_proche[0])
            position_actuelle = plus_proche[1]
            non_visites.remove(plus_proche)
        
        return ordre_visite

class VueGraphe(QWidget):
    def __init__(self):
        super().__init__()
        self.position_actuelle = (37, 3)  # Position de départ
        self.graphe.cellules_graphiques[self.position_actuelle].marquer_comme_entree()

    def recalculer_chemin_automatique(self):
        """Recalcule et affiche automatiquement le chemin optimal"""
        if not self.liste_courses:
            self.effacer_chemin()
            return
        
        # Effacer l'ancien chemin
        self.effacer_chemin()
        
        # Optimiser l'ordre de visite
        destinations = [(produit, self.produits_couloirs[produit]) 
                      for produit in self.liste_courses 
                      if produit in self.produits_couloirs]
        
        ordre_optimal = OptimiseurTSP.optimiser_ordre_visite(self.position_actuelle, destinations)
        
        # Calculer le chemin optimal
        position_actuelle = self.position_actuelle
        chemin_complet = []
        couleurs = [
            QColor(255, 107, 107),  # Rouge
            QColor(78, 205, 196),   # Turquoise
            QColor(69, 183, 209),   # Bleu
            QColor(150, 206, 180),  # Vert
            QColor(255, 234, 167),  # Jaune
            QColor(255, 159, 243),  # Rose
            QColor(189, 195, 199),  # Gris
            QColor(230, 126, 34),   # Orange
        ]
        
        numero_ordre = 1
        distance_totale = 0
        
        for i, produit in enumerate(ordre_optimal):
            if produit in self.produits_couloirs:
                position_produit = self.produits_couloirs[produit]
                
                # Calculer le chemin vers ce produit
                chemin = AlgorithmeDijkstra.dijkstra(
                    self.grille_logique, 
                    position_actuelle, 
                    position_produit
                )
                
                if chemin:
                    couleur = couleurs[i % len(couleurs)]
                    
                    # Afficher le chemin (sans compter les positions déjà visitées)
                    for coord in chemin:
                        if coord not in chemin_complet:
                            x, y = coord
                            if y < len(self.grille_cellules) and x < len(self.grille_cellules[0]):
                                self.grille_cellules[y][x].marquer_comme_chemin(couleur, numero_ordre)
                                numero_ordre += 1
                    
                    chemin_complet.extend(chemin)
                    distance_totale += len(chemin)
                    position_actuelle = position_produit
        
        # Mettre à jour les informations
        self.label_info.setText(
            f"Distance totale: {distance_totale} cases\n"
            f"Produits: {len(self.liste_courses)}\n"
            f"Ordre optimisé automatiquement"
        )
    
    def effacer_chemin(self):
        """Efface le chemin affiché sur la grille"""
        for ligne in self.grille_cellules:
            for cellule in ligne:
                if cellule.est_chemin:
                    cellule.reinitialiser()