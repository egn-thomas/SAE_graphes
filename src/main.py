import sys
from PyQt6.QtWidgets import QApplication
from controllerAdmin import MagasinController
from controllerClient import ClientController
from login import PageConnexion

def main():
    app = QApplication(sys.argv)

    login_dialog = PageConnexion()
    if login_dialog.exec():
        if login_dialog.role == "admin":
            controller = MagasinController()
        elif login_dialog.role == "client":
            controller = ClientController()
        else:
            print("Rôle inconnu, fermeture.")
            sys.exit()
        controller.vue.show()
        sys.exit(app.exec())
    else:
        print("Connexion annulée.")
        sys.exit()

if __name__ == "__main__":
    main()