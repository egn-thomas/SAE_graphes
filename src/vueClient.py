from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QFileDialog, QVBoxLayout, QLabel
from graphe import Graphe
from droparea import DropArea
from modelAdmin import MagasinModel
import os
import csv


class VueClient(QtWidgets.QWidget):
    """Vue principale de l'interface client"""
    def __init__(self):
        """Initialise l'interface utilisateur"""
        super(VueClient, self).__init__()
        self.setWindowTitle("L'interface utilisateur")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Cette page n'est pas développée")
        layout.addWidget(self.label)

        self.setLayout(layout)