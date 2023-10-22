from PyQt6 import QtWidgets, QtCore

class CategoriesBtn:
    def __init__(self, parent_widget, layout, database, project_id):
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
            self.category_buttons.append(button)

        return self.category_buttons

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        if self.category_buttons:
            for button in self.category_buttons:
                button_name = button.text()
                button.setText(_translate("MainWindow", button_name))