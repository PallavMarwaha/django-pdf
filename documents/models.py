from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class PDFDocument(models.Model):
    """
    Model for user uploaded PDF document. Linked to the user with a foreign key.
    """

    title = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to="docs/")

    def __str__(self) -> str:
        return self.title


class TextDocument(models.Model):
    """
    Model for generated text from the PDF document
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.ForeignKey("PDFDocument", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title
