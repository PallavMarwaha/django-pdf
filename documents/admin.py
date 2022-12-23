from django.contrib import admin
from .models import PDFDocument, TextDocument


@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]


@admin.register(TextDocument)
class TextDocumentAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]


# Register your models here.

# admin.site.register(PDFDocument)
# admin.site.register(TextDocument)
