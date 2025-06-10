import sys
from PyQt6.QtWidgets import QApplication, QInputDialog,QMessageBox,QLineEdit
from controllerAdmin import MagasinController


def mot_de_passe(max_attempts=3):
    for attempt in range(max_attempts):
        password, ok = QInputDialog.getText(None, "Authentification", f"Tentative {attempt + 1}/{max_attempts}\nEntrez le mot de passe:", echo=QLineEdit.EchoMode.Password)
        if ok and password == "mot":
            return True
        elif ok: 
            QMessageBox.warning(None, "Erreur", "Mot de passe incorrect")
        else:
            return False
    QMessageBox.critical(None, "Bloqué", "Trop de tentatives échouées !")
    return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if mot_de_passe():
        controller = MagasinController()
        controller.vue.show()
        app.exec()
    else:
        print("Authentification échouée ou annulée")
        sys.exit()



    