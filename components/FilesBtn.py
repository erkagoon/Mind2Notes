from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject, pyqtSignal
from functools import partial

class FilesBtn:
    def __init__(self, parent_widget, layout, database, categories_id):
        self.parent_widget = parent_widget
        self.layout = layout
        self.database = database
        self.categories_id = categories_id
        self.file_buttons = []

    def create_buttons(self):
        files = self.database.fetch_by_category_id(self.categories_id)

        if not files:
            label = QtWidgets.QLabel("Aucun fichier disponible pour cette catégorie.", self.parent_widget)
            self.layout.addWidget(label, 0, 0, 1, 2)
            return self.file_buttons

        for i, file in enumerate(files):
            button = QtWidgets.QPushButton(parent=self.parent_widget)
            button.setText(file[1])  # Supposons que l'index 1 est le nom du fichier.
            button.setObjectName(f"fileButton_{file[0]}")  # Supposons que l'index 0 est l'ID du fichier.
            sizePolicy = button.sizePolicy()
            sizePolicy.setVerticalPolicy(QtWidgets.QSizePolicy.Policy.Preferred)
            button.setSizePolicy(sizePolicy)
            row = i // 2
            col = i % 2
            self.layout.addWidget(button, row, col, 1, 1)
            self.file_buttons.append(button)

        return self.file_buttons

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        if self.file_buttons:
            for button in self.file_buttons:
                button_name = button.text()
                button.setText(_translate("MainWindow", button_name))
