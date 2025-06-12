from PyQt6.QtCore import QObject
# from modelClient import ClientModel
from vueClient import VueClient


class ClientController(QObject):
    def __init__(self):
        self.vue = VueClient()