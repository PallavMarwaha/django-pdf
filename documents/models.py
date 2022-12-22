from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField()


class TextDocument(models.Model):
    """
    Model for generated text from the PDF document
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.ForeignKey("PDFDocument", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
