import sys
from PyQt6.QtWidgets import QApplication
from controllerAdmin import MagasinController
from login import PageConnexion

def main():
    app = QApplication(sys.argv)

    connexion = PageConnexion()
    if connexion.exec():
        controller = MagasinController()
        controller.vue.show()
        sys.exit(app.exec())
    else:
        print("Connexion échouée.")
        sys.exit()

if __name__ == "__main__":
    main()