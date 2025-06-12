from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

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

        self.role = None  # Peut être "admin" ou "client"

    def verifier_identifiant(self):
        identifiant = self.identifiant_input.text().strip().lower()
        if identifiant == "admin":
            self.role = "admin"
            self.accept()
        elif identifiant == "client":
            self.role = "client"
            self.accept()
        else:
            self.label.setText("Identifiant inconnu")