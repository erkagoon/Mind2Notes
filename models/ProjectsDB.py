from models.BaseDB import BaseDB
import sqlite3
import os

class ProjectsDB(BaseDB):
    def __init__(self, db_name):
        # Obtenez le chemin du répertoire où se trouve ce fichier
        dir_path = os.path.dirname(os.path.abspath(__file__))
        # Créez le chemin complet vers la base de données
        full_db_path = os.path.join(dir_path, db_name)

        super().__init__(full_db_path)
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def insert(self, name):
        try:
            self.cursor.execute("INSERT INTO projects (name) VALUES (?)", (name,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion: {e}")

    def delete(self, id):
        try:
            self.cursor.execute("DELETE FROM projects WHERE id=?", (id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression: {e}")

    def update(self, id, name=None):
        try:
            if name:
                self.cursor.execute("UPDATE projects SET name=? WHERE id=?", (name, id))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour: {e}")

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM projects")
        return self.cursor.fetchall()