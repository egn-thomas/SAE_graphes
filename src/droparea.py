from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt
import csv
import time
import os

class DropArea(QLabel):
    placer_produit = pyqtSignal(int, int, str)
    cellule_cliquee = pyqtSignal(int, int)
    parent = None
    
    def __init__(self, parent, est_rayon):
        super().__init__(parent)
        self.est_rayon = est_rayon
        self.setAcceptDrops(True)
        
        self.est_rayon = False
        
        self.default_style = """
            background-color: transparent;
            border: 1px solid rgba(0, 0, 0, 0.3);
        """
        self.hover_style_rayon = """
            background-color: rgba(10, 100, 10, 1);
            border: 1px solid rgba(255, 255, 255, 0.5);
        """
        self.hover_style_couloir = """
            background-color: rgba(100, 10, 10, 1);
            border: 1px solid rgba(255, 255, 255, 0.5);
        """
        self.filled_style = """
            background-color: rgba(10, 10, 100, 0.7);
            color: transparent;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """
        self.setStyleSheet(self.default_style)
        self.ligne = 0
        self.colonne = 0

    def lier_cellule(self, cellule):
        self.est_rayon = cellule.est_rayon

    def enterEvent(self, event):
        """Appelé quand la souris entre dans la zone"""
        if not self.text():
            if self.est_rayon == True:
                self.setStyleSheet(self.hover_style_rayon)
            else:
                self.setStyleSheet(self.hover_style_couloir)
        super().enterEvent(event)

    def dragEnterEvent(self, event):
        """Appelé quand un élément est glissé au-dessus"""
        if event.mimeData().hasText():
            if not self.text():
                if self.est_rayon == True:
                    self.setStyleSheet(self.hover_style_rayon)
                else:
                    self.setStyleSheet(self.hover_style_couloir)
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """Appelé quand l'élément quitte la zone"""
        if not self.text():
            self.setStyleSheet(self.default_style)
        super().dragLeaveEvent(event)

    def leaveEvent(self, event):
        """Appelé quand la souris quitte la zone"""
        if not self.text():    
            self.setStyleSheet(self.default_style)
        super().leaveEvent(event)

    def dropEvent(self, event):
        produit = event.mimeData().text()
        if self.est_rayon == True:
            self.setText(produit)
            self.setStyleSheet(self.filled_style)
            self.placer_produit.emit(self.ligne, self.colonne, produit)

            if hasattr(self, 'articles') and isinstance(self.articles, list):
                self.articles.append(produit)
            else:
                self.articles = [produit]
            event.acceptProposedAction()
            self.enregistrer_produit(produit)
        else:
            return
        
    def mousePressEvent(self, event):
        """Gère le clic sur la cellule uniquement si elle affiche un produit"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Si le texte est vide, aucun produit n'est enregistré
            if self.text().strip() != "":
                self.cellule_cliquee.emit(self.ligne, self.colonne)
            
    def enregistrer_produit(self, produit):
        """
        Enregistre le produit déposé dans le CSV avec les coordonnées formatées.
        Si le fichier CSV n'existe pas ou est vide, il est initialisé avec un en-tête incluant la colonne 'Nom du projet'.
        """
        try:
            # Récupérer le nom du projet depuis la vue administrateur, si disponible
            if hasattr(self, "vue_admin") and self.vue_admin is not None:
                nom_projet = self.vue_admin.nom_magasin.text()
                if not nom_projet:
                    nom_projet = ""
            else:
                nom_projet = ""
        
           
            x = self.colonne
            y = str(self.ligne)
            coord_formatee = f"{x}{y}"

            script_dir = os.path.dirname(os.path.abspath(__file__))
            chemin = os.path.join(script_dir, "..", "magasins/sauvegarde_rapide.csv")
            file_path = chemin
            header = ["Nom du projet", "Nom du produit", "X", "Y", "Position"]

            # Vérifier si le fichier existe et déterminer s'il est vide
            file_exists = os.path.exists(file_path)
            file_empty = not file_exists or os.stat(file_path).st_size == 0

            with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # S'il est vide, écrire l'en-tête
                if file_empty:
                    writer.writerow(header)
                # Écriture de la ligne contenant le nom du projet et le produit
                writer.writerow([nom_projet, produit, x, y, coord_formatee])

        except Exception as e:
            print(f"[ERREUR] Problème lors de l'enregistrement du produit {produit}: {e}")
            
    def mettre_a_jour_apparence(self):
        if not hasattr(self, "articles") or not self.articles:
            self.setStyleSheet(self.default_style)
            self.setText(None)
        else:
            self.setStyleSheet(self.filled_style)