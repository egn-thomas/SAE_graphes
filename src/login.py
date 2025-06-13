import os
import json
from hashlib import md5
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from vueAdmin import VueAdmin
from vueClient import VueClient

def hachage(chaine: str) :
    """
    Calcule et retourne le hachage MD5 de la chaîne passée en argument.
    Remarque : MD5 ne doit pas être utilisé pour des applications nécessitant une sécurité élevée.
    """
    return md5(chaine.encode()).hexdigest()

class PageConnexion(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        # Taille suffisante pour deux champs de saisie et un bouton
        self.setFixedSize(300, 220)

        layout = QVBoxLayout()

        # Champ pour l'identifiant
        self.label_identifiant = QLabel("Identifiant :")
        self.identifiant_input = QLineEdit()
        layout.addWidget(self.label_identifiant)
        layout.addWidget(self.identifiant_input)

        # Champ pour le mot de passe
        self.label_motdepasse = QLabel("Mot de passe :")
        self.motdepasse_input = QLineEdit()
        # Masquer le mot de passe saisi
        self.motdepasse_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.label_motdepasse)
        layout.addWidget(self.motdepasse_input)

        # Bouton de connexion
        self.bouton_connexion = QPushButton("Se connecter")
        self.bouton_connexion.clicked.connect(self.verifier_identifiants)
        layout.addWidget(self.bouton_connexion)

        self.setLayout(layout)
        self.role = None  # Ce membre servira pour stocker le rôle de l'utilisateur connecté

        # Chargement des utilisateurs depuis le fichier JSON
        self.utilisateurs = self.charger_utilisateurs()

    def charger_utilisateurs(self) :
        """
        Lit et retourne les données utilisateurs depuis le fichier login.json.
        Le fichier JSON doit être organisé ainsi :
        {
            "nom_utilisateur": {
                "password": "hachage_md5_du_motdepasse",
                "role": "role_utilisateur"
            },
            ...
        }
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            chemin = os.path.join(script_dir, "..", "login.json")
            with open(chemin, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print("Erreur lors du chargement du fichier JSON :", e)
            return {}

    def verifier_identifiants(self):
        """
        Récupère l'identifiant et le mot de passe saisis, calcule le hachage du mot de passe,
        puis compare avec les informations stockées dans le fichier JSON.
        Si la combinaison est correcte, le rôle associé est attribué et la fenêtre se ferme.
        Sinon, la connexion est rejetée.
        """
        # Traitement : l'identifiant est mis en minuscule pour uniformiser la comparaison
        identifiant = self.identifiant_input.text().strip().lower()

        motdepasse = self.motdepasse_input.text().strip()
        motdepasse_hash = hachage(motdepasse)

        if identifiant in self.utilisateurs:
            utilisateur = self.utilisateurs[identifiant]
            if utilisateur.get("password") == motdepasse_hash :
                # Récupération du rôle, si présent, et fermeture de la fenêtre de connexion
                self.role = utilisateur.get("role")
                self.accept()  # Connexion réussie
                print("conexion réussie")
                return
            else :
                QMessageBox.critical(self,"Erreur de connexion","Identifiant ou mot de passe incorrect")
        else :
            QMessageBox.critical(self,"Erreur de connexion","Identifiant ou mot de passe incorrect")

    def get_infos_connexion(self) :
        """Retourne le rôle de l'utilisateur connecté."""
        return self.role