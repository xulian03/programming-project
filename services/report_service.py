from project import User
from database.repository import RepositoryProvider

class ReportService:
    _instance = None

    def __init__(self):
        pass

    def generate_player_report():
        pass

    def export_to_csv(self, data, fileName):
        pass

    def get_instance():
        if ReportService._instance is None:
            ReportService._instance = ReportService()
        return ReportService._instance