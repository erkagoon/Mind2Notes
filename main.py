from PyQt6 import QtWidgets, QtCore
from Ui import Ui  # Import du module ui
from Ui.Overlay import Overlay  # Import du module ui
from components.Record import Record
from components.WhisperTranscriber import WhisperTranscriber
from components.NoteProcessor import NoteProcessor
from components.VocalCommandsManager import VocalCommandsManager
from models.ProjectsDB import ProjectsDB
from models.CategoriesDB import CategoriesDB
from components.CategoriesBtn import CategoriesBtn
from components.ProjectsBtn import ProjectsBtn

class MyMainWindow(QtWidgets.QMainWindow, Ui.Ui_MainWindow):
    def __init__(self, projects_db, categories_db, *args, **kwargs):
        super(MyMainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        # Créer une instance de la classe Record
        self.recorder = Record()

        # Création des boutons de projet et catégorie dynamiquement à partir des class ProjectsBtn et CategoriesBtn
        self.projects_component = ProjectsBtn(self, self.verticalLayout_3, projects_db)
        self.project_buttons = self.projects_component.create_buttons()
        self.projects_component.retranslateUi(self)

        self.categories_component = CategoriesBtn(self, self.gridLayout_4, categories_db, 1)
        self.category_buttons = self.categories_component.create_buttons()
        self.categories_component.retranslateUi(self)


        # Connecter l'action 'actionnew_record' à une méthode spécifique
        #self.actionnew_record.triggered.connect(self.on_new_record_triggered)
        #self.actionnew_record.triggered.connect(self.on_record_note_pressed)
        #self.myButton.pressed.connect(self.my_method)

    # def retranslateUi(self, MainWindow):
    #     # Appel à la méthode originale
    #     Ui.Ui_MainWindow.retranslateUi(self, MainWindow)

    #     _translate = QtCore.QCoreApplication.translate

    #     # Votre code personnalisé pour les boutons de catégorie
    #     if hasattr(self, "category_buttons") and self.category_buttons:
    #         for button in self.category_buttons:
    #             button_name = button.text()
    #             button.setText(_translate("MainWindow", button_name))

    #     # Votre code personnalisé pour les boutons de projet
    #     if hasattr(self, "project_buttons") and self.project_buttons:
    #         for button in self.project_buttons:
    #             button_name = button.text()
    #             button.setText(_translate("MainWindow", button_name))

    def on_record_note_pressed(self):
        print("on_record_note_pressed")
        self.recorder.start_record()
        
    def on_record_note_released(self):
        record_path = self.recorder.stop_record()
        model_type = "small"
        transcriber = WhisperTranscriber(record_path, model_type, True)
        transcription = transcriber.transcribe()
        print(f"Raw transription : {transcription}")

        note_processor = NoteProcessor(transcription)
        cleaned_note = note_processor.clean_record()
        print(f"Cleaned result : {cleaned_note}")

    def on_record_vocal_command_pressed(self):
        print("on_record_vocal_command_pressed")
        self.recorder.start_record()
        
    def on_record_vocal_command_released(self):
        record_path = self.recorder.stop_record()
        model_type = "small"
        transcriber = WhisperTranscriber(record_path, model_type, True)
        transcription = transcriber.transcribe()
        print(f"Raw transription : {transcription}")

        vocal_commands = VocalCommandsManager(transcription)
        function_call = vocal_commands.execute_command()
        print(f"Function call : {function_call}")

    # def on_new_record_triggered(self):
    #     # action utilisant le bouton new_record
    #     self.recorder.start_record()

def main():
    app = QtWidgets.QApplication([])

    # Initialisation de la base de données
    projects_db = ProjectsDB('projectsAndCats.db')
    categories_db = CategoriesDB('projectsAndCats.db')

    ##################################### Exemple d'insert dans la db projectsAndCats ################################################
    # Liste des noms de projets à insérer
    # project_names = ["Projet Alpha", "Projet Beta", "Projet Gamma", "Projet Delta", "Projet Epsilon", "Projet Zeta", "Projet Eta", "Projet Theta"]

    # Insérer chaque projet dans la base de données
    # for project_name in project_names:
    #     projects_db.insert(project_name)
    ##################################################################################################################################

    ##################################### Exemple d'insert dans la db projectsAndCats ################################################
    # Liste des catégories à insérer
    # category_names = [
    #     'Labrador Retriever', 'Golden Retriever', 'German Shepherd', 'Beagle',
    #     'Bulldog', 'Poodle', 'Dachshund', 'Siberian Husky', 'Great Dane',
    #     'Boxer', 'Rottweiler', 'Doberman Pinscher'
    # ]

    # Insérer chaque catégorie dans la base de données pour le projet ayant l'ID 1
    # for category_name in category_names:
    #     categories_db.insert(category_name, 1)
    ##################################################################################################################################

    window = MyMainWindow(projects_db, categories_db)  # Utilisation de notre sous-classe personnalisée au lieu de QMainWindow
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
