from PyQt6 import QtWidgets
from Ui import Ui  # Import du module ui
from Ui.Overlay import Overlay  # Import du module ui
from components.Record import Record
from components.WhisperTranscriber import WhisperTranscriber
from components.NoteProcessor import NoteProcessor
from components.VocalCommandsManager import VocalCommandsManager
from models.ProjectsDB import ProjectsDB
from models.CategoriesDB import CategoriesDB

class MyMainWindow(QtWidgets.QMainWindow, Ui.Ui_MainWindow):
    def __init__(self, projects_db, categories_db, *args, **kwargs):
        super(MyMainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self, projects_db, categories_db)

        # Créer une instance de la classe Record
        self.recorder = Record()

        # Connecter l'action 'actionnew_record' à une méthode spécifique
        #self.actionnew_record.triggered.connect(self.on_new_record_triggered)
        #self.actionnew_record.triggered.connect(self.on_record_note_pressed)
        #self.myButton.pressed.connect(self.my_method)

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
