from django.db import models


class ClassifiedDocument(models.Model):
    CATEGORY_CHOICES = [
        ('identity_document', 'Identity Document'),
        ('employment_contract', 'Employment Contract'),
        ('payslip', 'Payslip'),
        ('invoice', 'Invoice'),
        ('tax_form', 'Tax Form'),
        ('other', 'Other'),
    ]
    CONFIDENCE_CHOICES = [('high','High'),('medium','Medium'),('low','Low')]

    filename        = models.CharField(max_length=255)
    category        = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    confidence      = models.CharField(max_length=10, choices=CONFIDENCE_CHOICES)
    extracted_fields= models.JSONField(default=dict)
    raw_text_preview= models.TextField(blank=True)
    model_used      = models.CharField(max_length=100)
    processing_time_ms = models.IntegerField()
    created_at      = models.DateTimeField(auto_now_add=True)