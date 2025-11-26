from django.db import models

class Document(models.Model):
    LANGUAGE_CHOICES = [
        ('Luo', 'Luo'),
        ('Kikuyu', 'Kikuyu'),
        ('Luhya', 'Luhya'),
        ('Kisii', 'Kisii'),
        ('Swahili', 'Swahili')
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    file = models.FileField(upload_to='documents/')
    target_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    translated_file = models.FileField(upload_to='translated/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.file.name} -> {self.target_language}"
