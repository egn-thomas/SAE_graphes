import sys
from PyQt6.QtWidgets import QApplication, QDialog
from controllerAdmin import MagasinController
from controllerClient import ClientController
from login import PageConnexion

def lancer_application_depuis_connexion(app):
    while True:
        connexion = PageConnexion()
      
        result = connexion.exec()  

        if result == QDialog.DialogCode.Accepted:
            role = connexion.get_infos_connexion()
            if role == "admin":
                controller = MagasinController()
            elif role == "client":
                controller = ClientController()
            else:
                print("Rôle inconnu.")
                continue
            controller.vue.show()
            app.exec()
            if getattr(controller, "retour_connexion", False):
                continue
            else:
                break
        else:


            break

def main():
    app = QApplication(sys.argv)
    lancer_application_depuis_connexion(app)
    sys.exit(0)

if __name__ == "__main__":
    main()
