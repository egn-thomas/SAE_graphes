from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt

class DropArea(QLabel):
    placer_produit = pyqtSignal(int, int, str)
    cellule_cliquee = pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            background-color: transparent;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
        """)
        self.ligne = 0
        self.colonne = 0

    def dragEnterEvent(self, event):
        """Active quand un élément est glissé au-dessus"""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Active quand un élément est déposé"""
        produit = event.mimeData().text()
        self.setText(produit)
        self.setStyleSheet("""
            background-color: rgba(100, 100, 100, 0.6);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)
        # Émettre le signal avec la position et le produit
        self.placer_produit.emit(self.ligne, self.colonne, produit)
        event.acceptProposedAction()

    def mousePressEvent(self, event):
        """Active quand la cellule est cliquée"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.cellule_cliquee.emit(self.ligne, self.colonne)