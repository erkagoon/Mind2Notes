from PyQt6 import QtWidgets
from Ui import Ui  # Import du module ui

def main():
    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui_instance = Ui.Ui_MainWindow()  # Créez une instance de l'interface utilisateur
    ui_instance.setupUi(MainWindow)
    MainWindow.show()
    app.exec()

if __name__ == "__main__":
    main()
