import sys
from PyQt6.QtWidgets import QApplication
from controllerAdmin import MagasinController
from controllerClient import ClientController
from login import PageConnexion

def lancer_application_depuis_connexion(app):
    while True:
        connexion = PageConnexion()
        if connexion.exec():
            role = connexion.get_infos_connexion()
            if role == "admin":
                controller = MagasinController()
                controller.vue.show()
                app.exec()
                if controller.retour_connexion:
                    continue
                else:
                    break
            elif role == "client":
                controller = ClientController()
                controller.vue.show()
                app.exec()
                if controller.retour_connexion:
                    continue
                else:
                    break
            else : 
                break
        else:
            break

def main():
    app = QApplication(sys.argv)
    lancer_application_depuis_connexion(app)
    sys.exit(0)

if __name__ == "__main__":
    main()
    