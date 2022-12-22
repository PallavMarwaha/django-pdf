from django.contrib import admin
from .models import PDFDocument, TextDocument

# Register your models here.

admin.site.register(PDFDocument)
admin.site.register(TextDocument)
