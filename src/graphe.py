from typing import Tuple, List, Dict
from cellule import Cellule
from droparea import DropArea
from typing import List, Tuple
import heapq
import csv
import os

class Graphe:
    """Représente le graphe du magasin et gère son affichage"""
    def __init__(self, nb_lignes: int, nb_colonnes: int, cases_colorees, parent=None):
        self.graphe = {}
        self.cellules_graphiques = {}
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.cases_colorees = cases_colorees
        self.parent = parent
        self.panier = {}
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

    def _creer_cellule_graphique(self, i, j, grille_vue=None):
        """Crée une cellule graphique"""
        est_rayon = (i, j) in self.cases_colorees
        drop_area = DropArea(self.parent, est_rayon)
        drop_area.ligne = i
        drop_area.colonne = j
        cellule_logique = self.graphe[(i, j)]
        drop_area.lier_cellule(cellule_logique)

        self.cellules_graphiques[(i, j)] = drop_area

        # Synchronise avec le dict de la vue si fourni
        if grille_vue is not None:
            grille_vue[(i, j)] = drop_area

    def afficher_grille(self, container_widget, grille_vue=None):
        """Affiche la grille graphiquement et lie les DropArea à la vue si grille_vue est fourni"""
        if not self.parent:
            return

        width = container_widget.width()
        height = container_widget.height()
        cell_width = width / self.nb_colonnes
        cell_height = height / self.nb_lignes

        # Crée les cellules graphiques AVANT de les afficher
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                self._creer_cellule_graphique(i, j, grille_vue)

        # Positionne les DropArea
        for (i, j), drop_area in self.cellules_graphiques.items():
            x = int(j * cell_width)
            y = int(i * cell_height)
            width_cell = int(cell_width) if j < self.nb_colonnes - 1 else (width - int(j * cell_width))
            height_cell = int(cell_height) if i < self.nb_lignes - 1 else (height - int(i * cell_height))

            drop_area.setGeometry(x, y, width_cell, height_cell)
            drop_area.show()
            
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


    def charger_catalogue_depuis_csv(self, nom_csv):
        """charge les articles du magasin sous forme de dictionnaire"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "..", nom_csv)
        with open(csv_path, mode='r', encoding='utf-8') as fichier:
            lecteur = csv.DictReader(fichier, delimiter=';')
            for ligne in lecteur:
                nom_produit = ligne['Nom du produit'].strip()
                try:
                    x = int(ligne['X'])
                    y = int(ligne['Y'])
                    self.panier[nom_produit] = (y, x)
                except ValueError:
                    continue
                print("Catalogue chargé :")
            for produit in self.panier:
                print("-", produit)
        return self.panier
    
    def trouver_voisin_libre(self, position: Tuple[int, int]) -> Tuple[int, int]:
        """Retourne une case voisine libre (non-rayon) pour une position donnée"""
        y, x = position
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # droite, bas, gauche, haut
        for dy, dx in directions:
            voisin = (y + dy, x + dx)
            cellule = self.graphe.get(voisin)
            if cellule and not cellule.est_rayon:
                return voisin
        return None

    def dijkstra_coordonnees(self, depart: Tuple[int, int], destination: Tuple[int, int]) -> List[Tuple[int,int]]:
        """Calcule le plus court chemin entre depart et destination en évitant les rayons"""
        distances = {depart: 0}
        predecesseurs = {}
        queue = [(0, depart)]

        while queue:
            cout_actuel, sommet = heapq.heappop(queue)
            if sommet == destination:
                break
            cellule = self.graphe[sommet]

            for voisin in cellule.voisins:
                pos_voisin = voisin.get_position()
                if voisin.est_rayon:
                    continue
                nouveau_cout = cout_actuel + 1
                if pos_voisin not in distances or nouveau_cout < distances[pos_voisin]:
                    distances[pos_voisin] = nouveau_cout
                    predecesseurs[pos_voisin] = sommet
                    heapq.heappush(queue, (nouveau_cout, pos_voisin))

        # Reconstruction du chemin
        chemin = []
        pos = destination
        while pos != depart:
            if pos not in predecesseurs:
                return []  # Pas de chemin
            chemin.append(pos)
            pos = predecesseurs[pos]
        chemin.append(depart)
        chemin.reverse()
        return chemin

    def generer_chemin_complet(self, liste_articles: List[str], position_depart: Tuple[int,int]):
        """Construit le chemin complet détaillé en évitant les rayons"""

        # Récupérer les positions brutes des articles dans le catalogue
        try:
            positions_brutes = [self.panier[nom] for nom in liste_articles]
        except KeyError as e:
            raise ValueError(f"Article inconnu dans le catalogue : {e.args[0]}")

        # Trouver une case libre accessible autour de chaque article
        positions_accessibles = []
        for pos in positions_brutes:
            case_libre = self.trouver_voisin_libre(pos)
            if case_libre is None:
                raise ValueError(f"Aucune case accessible autour de l'article à la position {pos}")
            positions_accessibles.append(case_libre)

        # Construire le chemin complet avec Dijkstra entre chaque étape
        chemin_complet = []
        etapes = [position_depart] + positions_accessibles
        for i in range(len(etapes) - 1):
            depart = etapes[i]
            arrivee = etapes[i+1]
            sous_chemin = self.dijkstra_coordonnees(depart, arrivee)
            if not sous_chemin:
                raise ValueError(f"Aucun chemin trouvé entre {depart} et {arrivee}")
            # Pour éviter doublons, on enlève le premier point sauf au début
            if chemin_complet:
                sous_chemin = sous_chemin[1:]
            chemin_complet.extend(sous_chemin)

        return chemin_complet