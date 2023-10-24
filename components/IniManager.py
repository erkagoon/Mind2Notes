import configparser

class IniManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.config = configparser.ConfigParser()
        self.config.read(filepath)

    def read_property(self, section, key):
        """
        Lire une propriété d'une section spécifiée.

        Args:
        - section (str): La section du fichier ini.
        - key (str): La clé de la propriété à lire.

        Returns:
        - str: La valeur de la propriété ou None si la section ou la clé n'existe pas.
        """
        try:
            return self.config[section][key]
        except KeyError:
            return None

    def update_property(self, section, key, value):
        """
        Mettre à jour une propriété dans une section spécifiée.

        Args:
        - section (str): La section du fichier ini.
        - key (str): La clé de la propriété à mettre à jour.
        - value (str): La nouvelle valeur pour la propriété.
        """
        if section not in self.config:
            self.config.add_section(section)
        self.config[section][key] = value

        # Enregistrez les modifications dans le fichier
        with open(self.filepath, 'w') as configfile:
            self.config.write(configfile)

# Exemple d'utilisation
# ini_manager = IniManager('config.ini')
# print(ini_manager.read_property('DEFAULT', 'ServerAliveInterval'))  # Lire une propriété
# ini_manager.update_property('DEFAULT', 'ServerAliveInterval', '60')  # Mettre à jour une propriété
