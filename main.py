from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon
from PyQt6.QtCore import Qt
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
    def __init__(self, app, projects_db, categories_db, *args, **kwargs):
        super(MyMainWindow, self).__init__(*args, **kwargs)

        self.app = app

    ########### Mise en arrière plan de l'application #############
        # Créez une icône pour l'application
        icon_path = "icons/notebook.png"
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)

        # Créez un menu pour l'icône de plateau
        self.tray_menu = QMenu(self)

        show_action = QAction("Afficher", self)
        show_action.triggered.connect(self.show_window)
        self.tray_menu.addAction(show_action)

        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.app.quit)
        self.tray_menu.addAction(exit_action)

        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
    ###############################################################

        self.categories_db = categories_db
        self.setupUi(self)

        # Créer une instance de la classe Record
        self.recorder = Record()

        # Création des boutons de projet et catégorie dynamiquement à partir des class ProjectsBtn et CategoriesBtn
        self.projects_component = ProjectsBtn(self, self.verticalLayout_3, projects_db)
        self.project_buttons = self.projects_component.create_buttons()
        self.projects_component.project_button_clicked.connect(self.refresh_categories)
        self.projects_component.retranslateUi(self)

        self.categories_component = CategoriesBtn(self, self.gridLayout_4, categories_db, 1)
        self.category_buttons = self.categories_component.create_buttons()
        self.categories_component.retranslateUi(self)


        # Connecter l'action 'actionnew_record' à une méthode spécifique
        #self.actionnew_record.triggered.connect(self.on_new_record_triggered)
        #self.actionnew_record.triggered.connect(self.on_record_note_pressed)
        #self.myButton.pressed.connect(self.my_method)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Double-click
            self.show()

    def show_window(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()

    def refresh_categories(self, project_id):
        self.clear_layout(self.gridLayout_4)
        self.categories_component = CategoriesBtn(self, self.gridLayout_4, self.categories_db, project_id)
        self.category_buttons = self.categories_component.create_buttons()
        self.categories_component.retranslateUi(self)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

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

    def closeEvent(self, event):
        event.ignore()
        self.hide()

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
    # project_names = ["Chats", "Chiens", "Oiseaux", "Fourmis", "Cervidés", "Vaches", "Chevaux", "Animaux de la ferme"]

    # Insérer chaque projet dans la base de données
    # for project_name in project_names:
    #     projects_db.insert(project_name)
    ##################################################################################################################################

    ##################################### Exemple d'insert dans la db projectsAndCats ################################################
    # categories_lists = [
    #     ['Chat siamois', 'Chat persan', 'Chat Maine Coon', 'Chat sphynx', 'Chat bengal', 'Chat ragdoll', 'Chat britannique', 'Chat abyssin', 'Chat birman', 'Chat oriental', 'Chat norvégien', 'Chat chartreux'],
    #     ['Labrador Retriever', 'Golden Retriever', 'Berger allemand', 'Beagle', 'Bulldog', 'Caniche', 'Teckel', 'Husky sibérien', 'Grand Danois', 'Boxer', 'Rottweiler', 'Doberman'],
    #     ['Canari', 'Perruche ondulée', 'Cacatoès', 'Ara', 'Conure', 'Cockatiel', 'Amazone', 'Grue couronnée', 'Toucan', 'Colibri', 'Merle', 'Chouette'],
    #     ['Fourmi charpentière', 'Fourmi d\'Argentine', 'Fourmi de feu', 'Fourmi pharaon', 'Fourmi à miel', 'Fourmi moissonneuse', 'Fourmi noire de jardin', 'Fourmi rouge', 'Fourmi voleuse', 'Fourmi de velours', 'Fourmi jaune citron', 'Fourmi d\'odeur'],
    #     ['Cerf', 'Renne', 'Élan', 'Chevreuil', 'Daim', 'Caribou', 'Chital', 'Muntjac', 'Sambar', 'Cerf élaphe', 'Pudu', 'Rusa'],
    #     ['Vache holstein', 'Vache jersey', 'Vache angus', 'Vache hereford', 'Vache charolaise', 'Vache limousine', 'Vache belted galloway', 'Vache texas longhorn', 'Vache ayrshire', 'Vache guernsey', 'Vache simmental', 'Vache brahman'],
    #     ['Cheval arabe', 'Cheval quarter horse', 'Cheval andalou', 'Cheval pur-sang', 'Cheval appaloosa', 'Cheval miniature', 'Cheval mustang', 'Cheval tennessee walker', 'Cheval morgan', 'Cheval fjord', 'Cheval clydesdale', 'Cheval lippizan'],
    #     ['Poule', 'Coq', 'Canard', 'Dinde', 'Oie', 'Chèvre', 'Mouton', 'Porcelet', 'Vache', 'Cheval', 'Lapin', 'Pigeon']
    # ]

    # Insérer chaque catégorie dans la base de données pour le projet ayant l'ID project_id
    # for project_id, categories in enumerate(categories_lists, start=1):
    #     for category_name in categories:
    #         categories_db.insert(category_name, project_id)
    ##################################################################################################################################

    window = MyMainWindow(app, projects_db, categories_db)  # Utilisation de notre sous-classe personnalisée au lieu de QMainWindow
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
