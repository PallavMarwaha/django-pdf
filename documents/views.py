import os

import PyPDF2
import pypdfium2 as pdfium
from django.contrib.auth.decorators import login_required
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


def check_file_ext(file):
    """
    Returns the extension of the file. NOT SECURE.
    """
    file_name: str = file.name
    file_extension = file_name.split(".")[-1]

    if file_extension == "pdf":
        return "pdf"
    else:
        return "image"


def ocr(file):
    """
    Returns the converted text from either a PDF or an Image
    """
    # If the file type is PDF
    if check_file_ext(file) == "pdf":
        doc = pdfium.PdfDocument(file)
        # Check if the PDF contains more than one page
        if len(doc) > 1:
            return None
        else:
            page = doc.get_page(0)
            pil_image = page.render_to(
                pdfium.BitmapConv.pil_image,
            )
            content = ""
            pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
            image_text = pytesseract.image_to_string(pil_image)

            content = image_text
            return content

    # If the file type is IMAGE
    elif check_file_ext(file) == "image":
        doc = Image.open(file)
        content = ""

        pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

        image_text = pytesseract.image_to_string(doc)

        content = image_text
        return content


@login_required(login_url="users:user-login")
def document_upload(request):
    """
    Render the form for document upload and saves the converted text in the DB.
    """
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
