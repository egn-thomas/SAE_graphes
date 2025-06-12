from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class PageConnexion(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Mot de passe :")
        self.mot_de_passe = QLineEdit()
        self.mot_de_passe.setEchoMode(QLineEdit.EchoMode.Password)

        self.bouton_connexion = QPushButton("Se connecter")
        self.bouton_connexion.clicked.connect(self.verifier_mot_de_passe)

        layout.addWidget(self.label)
        layout.addWidget(self.mot_de_passe)
        layout.addWidget(self.bouton_connexion)

        self.setLayout(layout)
        self.acces_autorise = False

    def verifier_mot_de_passe(self):
        if self.mot_de_passe.text() == "admin123":  # <- mot de passe à changer
            self.acces_autorise = True
            self.accept()
        else:
            self.label.setText("Mot de passe incorrect")