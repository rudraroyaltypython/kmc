from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload {self.id}"


class DailyAnalysis(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    ]

    date = models.DateField()
    day = models.CharField(max_length=3, choices=DAY_CHOICES)

    # LEFT vertical 3 digits → e.g. 7,9,9 → 799
    open_value = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)],
        help_text="3-digit vertical value (e.g. 799)"
    )

    # CENTER bold value → e.g. 51
    mid_value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        help_text="2-digit center value (e.g. 51)"
    )

    # RIGHT vertical 3 digits → e.g. 1,5,5 → 155
    close_value = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)],
        help_text="3-digit vertical value (e.g. 155)"
    )

    source = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='records'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'day']
        verbose_name = "Daily Analysis"
        verbose_name_plural = "Daily Analysis"

    def __str__(self):
        return f"{self.date} {self.day} | {self.open_value}-{self.mid_value}-{self.close_value}"
