import sys
from PyQt6.QtWidgets import QApplication
from controllerAdmin import MagasinController
from controllerClient import ClientController
from login import PageConnexion

def main():
    app = QApplication(sys.argv)
    login_dialog = PageConnexion()
    login_dialog.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    