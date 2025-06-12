from PyQt6.QtCore import QObject
# from modelClient import ClientModel
from vueClient import VueClient
from cellule import Cellule
from graphe import Graphe
from login import PageConnexion
import time


class ClientController(QObject):
    def __init__(self):
        self.vue = VueClient()