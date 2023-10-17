from PyQt6 import QtWidgets
from Ui import Ui  # Import du module ui
from Ui.Overlay import Overlay  # Import du module ui
from components.Record import Record

class MyMainWindow(QtWidgets.QMainWindow, Ui.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MyMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Créer une instance de la classe Record
        self.recorder = Record()

        # Connecter l'action 'actionnew_record' à une méthode spécifique
        self.actionnew_record.triggered.connect(self.on_new_record_triggered)

    def on_new_record_triggered(self):
        # action utilisant le bouton new_record
        self.recorder.start_record()

def main():
    app = QtWidgets.QApplication([])
    window = MyMainWindow()  # Utilisation de notre sous-classe personnalisée au lieu de QMainWindow
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
