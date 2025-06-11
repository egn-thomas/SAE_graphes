from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt

class DropArea(QLabel):
    placer_produit = pyqtSignal(int, int, str)
    cellule_cliquee = pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.default_style = """
            background-color: transparent;
            border: 1px solid rgba(0, 0, 0, 0.3);
        """
        self.hover_style_rayon = """
            background-color: rgba(10, 100, 10, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.5);
        """
        self.hover_style_couloir = """
            background-color: rgba(100, 10, 10, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.5);
        """
        self.filled_style = """
            background-color: rgba(10, 10, 100, 0.5);
            color: transparent;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """
        self.setStyleSheet(self.default_style)
        self.ligne = 0
        self.colonne = 0

    def lier_cellule(self, cellule):
        """Lie la DropArea à une cellule logique"""
        self.est_rayon = cellule.est_rayon

    def enterEvent(self, event):
        """Appelé quand la souris entre dans la zone"""
        if not self.text():
            if self.est_rayon:
                self.setStyleSheet(self.hover_style_rayon)
            else:
                self.setStyleSheet(self.hover_style_couloir)
        super().enterEvent(event)

    def dragEnterEvent(self, event):
        """Appelé quand un élément est glissé au-dessus"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def leaveEvent(self, event):
        """Appelé quand la souris quitte la zone"""
        if not self.text():    
            self.setStyleSheet(self.default_style)
        super().leaveEvent(event)

    def dropEvent(self, event):
        """Active quand un élément est déposé"""
        produit = event.mimeData().text()
        self.setText(produit)
        self.setStyleSheet(self.filled_style)
        self.placer_produit.emit(self.ligne, self.colonne, produit)
        event.acceptProposedAction()

    def mousePressEvent(self, event):
        """Gère le clic sur la cellule"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.cellule_cliquee.emit(self.ligne, self.colonne)