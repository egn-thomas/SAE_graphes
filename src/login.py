import os
import json
from hashlib import md5
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

def hachage(chaine: str) :
    return md5(chaine.encode()).hexdigest()

class PageConnexion(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setFixedSize(300, 200)  # Taille ajustée pour accueillir deux champs
        
        layout = QVBoxLayout()

        # Champ pour le nom d'utilisateur
        self.label_identifiant = QLabel("Identifiant :")
        self.identifiant_input = QLineEdit()
        layout.addWidget(self.label_identifiant)
        layout.addWidget(self.identifiant_input)

        # Champ pour le mot de passe
        self.label_motdepasse = QLabel("Mot de passe :")
        self.motdepasse_input = QLineEdit()
        self.motdepasse_input.setEchoMode(QLineEdit.EchoMode.Password)  # Masque la saisie du mot de passe
        layout.addWidget(self.label_motdepasse)
        layout.addWidget(self.motdepasse_input)

        # Bouton de connexion
        self.bouton_connexion = QPushButton("Se connecter")
        self.bouton_connexion.clicked.connect(self.verifier_identifiants)
        layout.addWidget(self.bouton_connexion)

        self.setLayout(layout)
        
        # Chargement des utilisateurs depuis le fichier JSON
        self.utilisateurs = self.charger_utilisateurs()
        
    


    def charger_utilisateurs(self):
        """
        Lit et retourne les identifiants et mots de passe hachés depuis le fichier login.json.
        Le fichier JSON doit être organisé sous la forme :
        {
            "nom_utilisateur": "hachage_mot_de_passe",
            ...
        }
        """
        try:
            with open("login.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print("Erreur lors du chargement du fichier JSON :", e)
            return {}

    def verifier_identifiants(self):
        """
        Récupère le nom d'utilisateur et le mot de passe saisis, hache ce dernier,
        puis compare avec les données provenant du fichier JSON.
        Si la combinaison est correcte, la fenêtre se ferme en acceptant, sinon en rejetant.
        """
        identifiant = self.identifiant_input.text().strip().lower()
        motdepasse = self.motdepasse_input.text().strip()
        motdepasse_hash = hachage(motdepasse)

        if identifiant in self.utilisateurs and self.utilisateurs[identifiant] == motdepasse_hash:
            self.accept()  # Connexion réussie
        else:
            print("Identifiant ou mot de passe incorrect")
            self.reject()  # Connexion échouée
            
