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
            name TEXT NOT NULL,
            description TEXT
        )
        ''')
        self.conn.commit()

    def insert(self, name, description=None):
        try:
            self.cursor.execute("INSERT INTO projects (name, description) VALUES (?, ?)", (name, description))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion: {e}")


    def delete(self, id):
        try:
            self.cursor.execute("DELETE FROM projects WHERE id=?", (id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression: {e}")

    def update(self, id, name=None, description=None):
        try:
            updates = []
            parameters = []
            if name:
                updates.append("name=?")
                parameters.append(name)
            if description:
                updates.append("description=?")
                parameters.append(description)
            
            if updates:
                parameters.append(id)
                self.cursor.execute(f"UPDATE projects SET {', '.join(updates)} WHERE id=?", tuple(parameters))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour: {e}")


    def get(self, id):
        self.cursor.execute("SELECT * FROM projects WHERE id=?", (id,))
        return self.cursor.fetchone()
    
    def get_from_name(self, name):
        self.cursor.execute("SELECT * FROM projects WHERE name=?", (name,))
        return self.cursor.fetchone()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM projects")
        return self.cursor.fetchall()