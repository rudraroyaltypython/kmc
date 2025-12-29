from django.apps import AppConfig
from analyzer.services.probability_weights import init_weights


class AnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analyzer'

    def ready(self):
        # Update this path + column name as needed
        init_weights("media/uploads/history.xlsx", column_name="result")
