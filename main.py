from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon
from PyQt6.QtCore import Qt
from Ui import Ui  # Import du module ui
from Ui.Overlay import Overlay  # Import du module ui
from Ui.Setting import Ui_Form
from components.Record import Record
from components.WhisperTranscriber import WhisperTranscriber
from components.NoteProcessor import NoteProcessor
from components.VocalCommandsManager import VocalCommandsManager
from models.ProjectsDB import ProjectsDB
from models.CategoriesDB import CategoriesDB
from models.FilesDB import FilesDB
from components.CategoriesBtn import CategoriesBtn
from components.ProjectsBtn import ProjectsBtn
from mainSetting import SettingWindow
from core.MyMainWindow import MyMainWindow

def main():
    app = QtWidgets.QApplication([])

    # Initialisation de la base de données
    projects_db = ProjectsDB('projectsAndCats.db')
    categories_db = CategoriesDB('projectsAndCats.db')
    files_db = FilesDB('projectsAndCats.db')
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

    # Exemple d'insert de fichiers dans la db projectsAndCats
    # Les fichiers pour le projet 1, catégorie 1
    # files_to_insert_project1_cat1 = [
    #     ('fichier1_projet1_cat1.jpg', 1, 1),
    #     ('fichier2_projet1_cat1.jpg', 1, 1)
    # ]

    # # Les fichiers pour le projet 1, catégorie 2
    # files_to_insert_project1_cat2 = [
    #     ('fichier1_projet1_cat2.jpg', 1, 2),
    #     ('fichier2_projet1_cat2.jpg', 1, 2)
    # ]

    # # Insérer les fichiers pour le projet 1, catégorie 1
    # for file_name, project_id, category_id in files_to_insert_project1_cat1:
    #     files_db.insert(file_name, project_id, category_id)

    # # Insérer les fichiers pour le projet 1, catégorie 2
    # for file_name, project_id, category_id in files_to_insert_project1_cat2:
    #     files_db.insert(file_name, project_id, category_id)

    main_window = MyMainWindow(app, projects_db, categories_db, files_db)
    main_window.show()
    app.exec()

if __name__ == "__main__":
    main()
