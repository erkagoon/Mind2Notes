from PyQt6 import QtWidgets, QtCore, QtGui
from Ui.Setting import Ui_Form
from components.IniManager import IniManager

class CustomLineEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(CustomLineEdit, self).__init__(*args, **kwargs)
        self.setReadOnly(True)  # Bloquer l'écriture
        self.pressed_keys = set()
        self.is_clicked = False
        self.setStyleSheet("QLineEdit { border: 1px solid gray; } QLineEdit:focus { border: 1px solid blue; }")  # Ajoute un style pour indiquer le focus

    def mousePressEvent(self, event):
        super(CustomLineEdit, self).mousePressEvent(event)
        self.is_clicked = True
        self.setFocus()  # Mettre le QLineEdit en surbrillance

    def keyPressEvent(self, event):
        if not self.is_clicked:
            return

        key = event.key()
        main_key = QtGui.QKeySequence(key).toString()

        # Ajouter les modificateurs
        if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
            self.pressed_keys.add("Ctrl")
        if event.modifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.pressed_keys.add("Shift")
        if event.modifiers() & QtCore.Qt.KeyboardModifier.AltModifier:
            self.pressed_keys.add("Alt")

        # Ajouter la touche principale si ce n'est pas un modificateur
        mod_keys = ["Ctrl", "Shift", "Alt", "Meta", "Control"]  # Adding "Control" to the list
        if main_key not in mod_keys:
            self.pressed_keys.add(main_key)

    def keyReleaseEvent(self, event):
        if not self.is_clicked:
            return

        # Si toutes les touches sont relâchées, affichez la combinaison
        if not event.modifiers():
            keys_combination = "+".join(sorted(self.pressed_keys))
            self.setText(keys_combination)
            self.pressed_keys.clear()
            self.is_clicked = False
            return


class SettingWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(SettingWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.customize_ui()

    def customize_ui(self):
        # Initialisation du gestionnaire INI
        ini_manager = IniManager('setting.ini')
        
        # Obtenir toutes les sections du fichier INI
        sections = ini_manager.config.sections()
        
        for section in sections:
            keys = ini_manager.config[section].keys()
            
            for key in keys:
                # Création et configuration du label
                label = QtWidgets.QLabel(parent=self)
                label.setFixedHeight(25)
                label.setText(f"{section} - {key}")
                self.verticalLayout_10.addWidget(label)
                
                # Création et configuration du line edit avec la valeur du setting.ini
                line_edit = CustomLineEdit(parent=self)
                line_edit.setFixedHeight(25)
                line_edit.setText(ini_manager.read_property(section, key))
                self.verticalLayout_11.addWidget(line_edit)

                line_edit.textChanged.connect(lambda value, section=section, key=key: self.update_ini_key(section, key, value))
        
        # Ajout des spacers
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_10.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_11.addItem(spacerItem1)

    def update_ini_key(self, section, key, value):
        """Mettre à jour une clé dans le fichier ini."""
        ini_manager = IniManager('setting.ini')
        ini_manager.update_property(section, key, value)
