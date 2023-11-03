class UIManager:
    @staticmethod
    def ui_instance():
        from core.MyMainWindow import MyMainWindow
        try:
            return MyMainWindow.get_instance()
        except Exception as e:
            print(f"Erreur lors de l'obtention de l'instance MyMainWindow: {e}")
            return None
        
    @staticmethod
    def refresh_projects():
        instance = UIManager.ui_instance()
        if instance is not None:
            instance.refresh_projects_needed.emit()

    @staticmethod
    def refresh_categories(project_id):
        instance = UIManager.ui_instance()
        if instance is not None:
            instance.refresh_categories_needed.emit(project_id)

