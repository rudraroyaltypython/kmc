from django.contrib import admin
from .models import UploadedFile, DailyAnalysis
from .services.excel_parser import parse_excel

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        records = parse_excel(obj.file.path, obj)
        DailyAnalysis.objects.bulk_create(
            [DailyAnalysis(**r) for r in records]
        )


@admin.register(DailyAnalysis)
class DailyAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'day',
        'open_value', 'mid_value', 'close_value'
    )
    list_filter = ('day', 'date')
