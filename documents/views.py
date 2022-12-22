from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import PDFDocumentForm
import PyPDF2
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from pytesseract import pytesseract
from .models import TextDocument, PDFDocument
from django.contrib.auth import get_user_model
from django.conf import settings
import os
import pypdfium2 as pdfium

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
