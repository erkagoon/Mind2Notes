from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon
from PyQt6.QtCore import Qt
from Ui import Ui  # Import du module ui
from components.Record import Record
from components.WhisperTranscriber import WhisperTranscriber
from components.NoteProcessor import NoteProcessor
from components.VocalCommandsManager import VocalCommandsManager
from components.CategoriesBtn import CategoriesBtn
from components.ProjectsBtn import ProjectsBtn
from mainSetting import SettingWindow

class MyMainWindow(QtWidgets.QMainWindow, Ui.Ui_MainWindow):
    _instance = None
    refresh_categories_needed = QtCore.pyqtSignal(int)
    refresh_projects_needed = QtCore.pyqtSignal()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise Exception("Instance not created yet")
        return cls._instance
    
    def __init__(self, app, projects_db, categories_db, *args, **kwargs):
        """Constructeur privé."""
        if MyMainWindow._instance is not None:
            raise Exception("Cette classe est un singleton !")
        super(MyMainWindow, self).__init__(*args, **kwargs)
        MyMainWindow._instance = self
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
        self.projects_db = projects_db
        self.setupUi(self)

        # Créer une instance de la classe Record
        self.recorder = Record()

        # Création des boutons de projet et catégorie dynamiquement à partir des class ProjectsBtn et CategoriesBtn
        self.projects_component = ProjectsBtn(self, self.projectContainer, projects_db)
        self.project_buttons = self.projects_component.create_buttons()
        self.projects_component.project_button_clicked.connect(self.refresh_categories)
        self.projects_component.retranslateUi(self)

        self.categories_component = CategoriesBtn(self, self.catsContainer, categories_db, 1)
        self.category_buttons = self.categories_component.create_buttons()
        self.categories_component.retranslateUi(self)

        # Bouton setting
        self.actionsetting.triggered.connect(self.open_settings_window)

        # Connecter l'action 'actionnew_record' à une méthode spécifique
        #self.actionnew_record.triggered.connect(self.on_new_record_triggered)
        #self.actionnew_record.triggered.connect(self.on_record_note_pressed)
        #self.myButton.pressed.connect(self.my_method)

        self.refresh_categories_needed.connect(self.refresh_categories)
        self.refresh_projects_needed.connect(self.refresh_projects)
        
    def open_settings_window(self):
        self.settings_window = SettingWindow()  # Utilisez SettingWindow au lieu de Ui_Form
        self.settings_window.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Double-click
            self.show()

    def show_window(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()

    def refresh_categories(self, project_id):
        self.clear_layout(self.catsContainer)
        self.categories_component = CategoriesBtn(self, self.catsContainer, self.categories_db, project_id)
        self.category_buttons = self.categories_component.create_buttons()
        self.categories_component.retranslateUi(self)

    def refresh_projects(self):
        self.clear_layout(self.projectContainer)
        self.projects_component = ProjectsBtn(self, self.projectContainer, self.projects_db)
        self.project_buttons = self.projects_component.create_buttons()
        self.projects_component.retranslateUi(self)

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
        # print(f"Function call : {function_call}")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    # def on_new_record_triggered(self):
    #     # action utilisant le bouton new_record
    #     self.recorder.start_record()
