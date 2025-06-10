import sys
from PyQt6.QtWidgets import QApplication
from controllerAdmin import MagasinController


def main():
    app = QApplication(sys.argv)
    controller = MagasinController()
    controller.view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()