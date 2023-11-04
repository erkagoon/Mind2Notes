from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject, pyqtSignal
from functools import partial

# Faites en sorte que CategoriesBtn hérite de QObject pour pouvoir utiliser les signaux
class CategoriesBtn(QObject):
    # Définissez un signal pyqtSignal avec un argument entier pour l'ID de la catégorie
    category_button_clicked = pyqtSignal(int)

    def __init__(self, parent_widget, layout, database, project_id):
        super().__init__()  # N'oubliez pas d'appeler le constructeur de la classe de base
        self.parent_widget = parent_widget
        self.layout = layout
        self.database = database
        self.project_id = project_id
        self.category_buttons = []

    def create_buttons(self):
        categories = self.database.fetch_by_project_id(self.project_id)

        if not categories:
            label = QtWidgets.QLabel("Aucune catégorie disponible pour ce projet.", self.parent_widget)
            self.layout.addWidget(label, 0, 0, 1, 2)
            return self.category_buttons

        for i, category in enumerate(categories):
            button = QtWidgets.QPushButton(parent=self.parent_widget)
            button.setText(category[1])
            button.setObjectName(f"categoryButton_{category[0]}")
            sizePolicy = button.sizePolicy()
            sizePolicy.setVerticalPolicy(QtWidgets.QSizePolicy.Policy.Preferred)
            button.setSizePolicy(sizePolicy)
            row = i // 2
            col = i % 2
            self.layout.addWidget(button, row, col, 1, 1)
            # Connectez le clic du bouton au signal en utilisant `partial` pour passer l'ID de la catégorie
            button.clicked.connect(partial(self.category_button_clicked.emit, category[0]))
            self.category_buttons.append(button)

        return self.category_buttons

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        if self.category_buttons:
            for button in self.category_buttons:
                button_name = button.text()
                button.setText(_translate("MainWindow", button_name))
