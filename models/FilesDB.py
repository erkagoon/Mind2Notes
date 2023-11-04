from models.BaseDB import BaseDB
import sqlite3
import os
from datetime import datetime

class FilesDB(BaseDB):
    def __init__(self, db_name):
        # Obtenez le chemin du répertoire où se trouve ce fichier
        dir_path = os.path.dirname(os.path.abspath(__file__))
        # Créez le chemin complet vers la base de données
        full_db_path = os.path.join(dir_path, db_name)

        super().__init__(full_db_path)
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            text TEXT NOT NULL,
            cat_id INTEGER,
            project_id INTEGER,
            date_create TEXT NOT NULL,
            FOREIGN KEY (cat_id) REFERENCES categories(id),
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
        ''')
        self.conn.commit()

    def insert(self, name, text, cat_id, project_id, date_create=None):
        if date_create is None:
            date_create = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute("INSERT INTO files (name, text, cat_id, project_id, date_create) VALUES (?, ?, ?, ?, ?)", 
                                (name, text, cat_id, project_id, date_create))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion: {e}")

    def delete(self, id):
        try:
            self.cursor.execute("DELETE FROM files WHERE id=?", (id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression: {e}")

    def update(self, id, name=None, text=None, cat_id=None, project_id=None, date_create=None):
        try:
            updates = []
            parameters = []
            if name:
                updates.append("name=?")
                parameters.append(name)
            if text:
                updates.append("text=?")
                parameters.append(text)
            if cat_id:
                updates.append("cat_id=?")
                parameters.append(cat_id)
            if project_id:
                updates.append("project_id=?")
                parameters.append(project_id)
            if date_create:
                updates.append("date_create=?")
                parameters.append(date_create)

            if updates:
                parameters.append(id)
                self.cursor.execute(f"UPDATE files SET {', '.join(updates)} WHERE id=?", tuple(parameters))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour: {e}")

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM files")
        return self.cursor.fetchall()

    def fetch_by_category_id(self, cat_id):
        self.cursor.execute("SELECT * FROM files WHERE cat_id=?", (cat_id,))
        return self.cursor.fetchall()

    def fetch_by_project_id(self, project_id):
        self.cursor.execute("SELECT * FROM files WHERE project_id=?", (project_id,))
        return self.cursor.fetchall()
