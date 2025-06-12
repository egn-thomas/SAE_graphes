from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from vueAdmin import VueAdmin
from vueClient import VueClient

class PageConnexion(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Identifiant :")
        self.identifiant_input = QLineEdit()

        self.bouton_connexion = QPushButton("Se connecter")
        self.bouton_connexion.clicked.connect(self.verifier_identifiant)

        layout.addWidget(self.label)
        layout.addWidget(self.identifiant_input)
        layout.addWidget(self.bouton_connexion)

        self.setLayout(layout)

        self.role = None

    def verifier_identifiant(self):
        identifiant = self.identifiant_input.text().strip().lower()
        if identifiant == "admin":
            self.ouvrir_vue_admin()
        elif identifiant == "client":
            self.ouvrir_vue_client()
        else:
            self.label.setText("Identifiant inconnu")
    
    def ouvrir_vue_admin(self):
        self.vue_admin = VueAdmin()
        self.vue_admin.show()
        self.close()
    
    def ouvrir_vue_client(self):
        self.vue_client = VueClient()
        self.vue_client.show()
        self.close()