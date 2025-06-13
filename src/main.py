import sys
from PyQt6.QtWidgets import QApplication, QDialog
from controllerAdmin import MagasinController
from controllerClient import ClientController
from login import PageConnexion

def lancer_application_depuis_connexion(app):
    while True:
        # Crée une nouvelle instance de la fenêtre de connexion
        connexion = PageConnexion()
        # Affiche la fenêtre de connexion de façon modale
        result = connexion.exec()  # Attend que l'utilisateur valide ou annule le dialogue

        if result == QDialog.DialogCode.Accepted:
            # Récupère le rôle via la méthode get_infos_connexion() de la classe PageConnexion
            role = connexion.get_infos_connexion()

            if role == "admin":
                controller = MagasinController()
            elif role == "client":
                controller = ClientController()
            else:
                # En cas de rôle inconnu, l'utilisateur est invité à retenter la connexion
                print("Rôle inconnu.")
                continue

            # Affiche la vue du contrôleur
            controller.vue.show()

            # Lance la boucle d'événements principale
            app.exec()

            # Lorsque la vue principale se ferme, on vérifie si l'utilisateur a demandé à se déconnecter
            if getattr(controller, "retour_connexion", False):
                # Si c'est le cas, on continue la boucle pour relancer le login
                continue
            else:
                break
        else:
            # Si le dialogue de connexion a été rejeté (annulé ou fermé), on quitte la boucle
            break

def main():
    app = QApplication(sys.argv)
    lancer_application_depuis_connexion(app)
    sys.exit(0)

if __name__ == "__main__":
    main()
