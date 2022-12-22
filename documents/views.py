import os

import PyPDF2
import pypdfium2 as pdfium
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from PIL import Image
from pytesseract import pytesseract

from .forms import PDFDocumentForm
from .models import PDFDocument, TextDocument

User = get_user_model()


def pdf_to_text(pdf_doc):

    # Read the file
    pdf = PyPDF2.PdfFileReader(pdf_doc)
    content = ""
    print(pdf.getNumPages())
    for ii in range(pdf.getNumPages()):
        # Get the page
        page = pdf.getPage(ii)
        print(page.extract_text())
        content += page.extract_text()

    print(content)

    return content


def ocr(file):
    doc = pdfium.PdfDocument(file)

    # Check if the PDF contains more than one page
    if len(doc) > 1:
        return None

    page = doc.get_page(0)
    pil_image = page.render_to(
        pdfium.BitmapConv.pil_image,
    )

    content = ""

    pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

    image_text = pytesseract.image_to_string(pil_image)

    content = image_text
    return content


def document_upload(request):

    if request.method == "POST":
        form = PDFDocumentForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            pdf_doc = request.FILES["document"]

            # Create PDF object
            pdf_obj = PDFDocument.objects.create(
                user=request.user, document=pdf_doc, title=pdf_doc.name
            )

            # Get the content from the PDF document
            content = ocr(file=pdf_doc)

            if content is None:
                print("PDF has more than one page")
                return HttpResponseRedirect(reverse("users:documents:document-upload"))

            # Create a TextDocument model
            TextDocument.objects.create(
                user=request.user, pdf=pdf_obj, title=pdf_doc.name, body=content
            )

            return HttpResponseRedirect(reverse("users:user-dashboard"))

    form = PDFDocumentForm()
    context = {"form": form}
    return render(request, "documents/upload.html", context=context)
