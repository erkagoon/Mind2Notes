from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject, pyqtSignal
from functools import partial

class ProjectsBtn(QObject):
    project_button_clicked = pyqtSignal(int)  # Signal avec l'ID du projet comme argument
    def __init__(self, parent_widget, layout, database):
        super().__init__()
        self.parent_widget = parent_widget
        self.layout = layout
        self.database = database
        self.project_buttons = []

    def create_buttons(self):
        projects = self.database.fetch_all()

        if not projects:
            label = QtWidgets.QLabel("Aucun projet disponible.", self.parent_widget)
            self.layout.addWidget(label)
            return self.project_buttons

        for project in projects:
            project_id, project_name = project
            button = QtWidgets.QPushButton(project_name, self.parent_widget)
            button.setObjectName(f"pushButton_{project_id}")
            button.clicked.connect(partial(self.project_button_clicked.emit, project_id))
            self.layout.addWidget(button)
            self.project_buttons.append(button)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacerItem)

        return self.project_buttons

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        if self.project_buttons:
            for button in self.project_buttons:
                button_name = button.text()
                button.setText(_translate("MainWindow", button_name))