import os

import cv2
import magic
import numpy as np
import PyPDF2
import pypdfium2 as pdfium
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from PIL import Image
from pytesseract import pytesseract

from .forms import PDFDocumentForm
from .models import PDFDocument, TextDocument

User = get_user_model()


def pdf_to_text(pdf_doc):
    """
    Helper function to convert PDF doc to Text doc using PyPDF2 module
    """
    # COMMENT: Obsolete helper function. Not in use anymore.

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
    Helper function which returns the extension of the file. NOT SECURE.
    """
    file_name: str = file.name
    file_extension = file_name.split(".")[-1]

    if file_extension == "pdf":
        return "pdf"
    else:
        return "image"


def ocr_old(file):
    """
    Helper function which returns the converted text from either a PDF or an Image. Uses Pillow image directly without any filters.
    """
    # COMMENT: Not being used anymore.
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
            image_text = pytesseract.image_to_string(pil_image, lang="eng")

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


def ocr(file):
    """
    Helper function which returns the converted text from either a PDF or an Image. Uses OpenCV and sharpening kernels.
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
            image_text = pytesseract.image_to_string(pil_image, lang="eng")

            content = image_text
            return content

    # If the file type is IMAGE
    elif check_file_ext(file) == "image":

        # Get Pillow image from the InMemory Stream
        pil_image = Image.open(file)

        # convert to CV2 image
        cv2_img = np.array(pil_image)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)

        # Convert to grayscale image, apply filters and sharpen the image using a sharpening kernel
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.threshold(
            sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )[1]

        content = ""

        pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

        # Convert the image to text using pytesseract
        image_text = pytesseract.image_to_string(thresh)

        content = image_text
        return content


def get_file_type(file):
    """
    Helper function to return the file type using python-magic module.
    """
    mime = magic.from_buffer(file.read(2048), mime=True)
    return mime


@login_required(login_url="users:user-login")
def document_upload(request):
    """
    Render the form for document upload and saves the converted text in the DB.
    """
    if request.method == "POST":
        form = PDFDocumentForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            pdf_doc = request.FILES["document"]

            # TODO: Return proper error messages to the front end.
            # To check if the file is valid
            if not (
                get_file_type(pdf_doc) == "application/pdf"
                or get_file_type(pdf_doc) == "image/png"
            ):
                print("The file is not in valid image/PDF format.")
                return HttpResponseRedirect(reverse("users:documents:document-upload"))

            if len(pdf_doc.name) > 50:
                short_pdf_name = f"{pdf_doc.name[0:30]}...{pdf_doc.name[-10:]}"
                pdf_doc.name = short_pdf_name

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


@login_required(login_url="users:user-login")
def text_detail_View(request, text_id):
    """
    Renders the document Text detail
    """
    # Check if the Text Document with the specified ID exists in the DB
    try:
        user = User.objects.get(username=request.user.username)
        text_doc = TextDocument.objects.get(id=text_id, user=user)
    except TextDocument.DoesNotExist:
        return HttpResponseRedirect(reverse("users:user-dashboard"))

    return render(
        request, "documents/document_details.html", context={"item": text_doc}
    )


@login_required(login_url="users:user-login")
def document_serve(request, text_id):
    """
    Serves the document in development by TextDocument ID and its corresponding PDF document
    """
    # Check if the Text Document with the specified ID exists in the DB
    try:
        user = User.objects.get(username=request.user.username)
        text_doc = TextDocument.objects.get(id=text_id, user=user)
    except TextDocument.DoesNotExist:
        return HttpResponseRedirect(reverse("users:user-dashboard"))

    # Get the TextDocument object and its related PDFDocument object wih foreign key relationship
    pdf_file = text_doc.pdf.document
    pdf_file_name = text_doc.pdf.title

    # NOTE: Don't know how to specify content type for HttpResponse for different file types like PDF, PNG and JPEG etc
    # Create a HttpResponse Object with the file
    response = HttpResponse(pdf_file)
    # Add file info like file name
    response["Content-Disposition"] = f"attachment; filename=  {pdf_file_name}"

    return response


@login_required(login_url="users:user-login")
def document_delete(request, doc_id):
    """
    Deletes the document with the specified ID
    """
    # Check if the Text Document with the specified ID exists in the DB
    try:
        user = User.objects.get(username=request.user.username)
        doc = PDFDocument.objects.get(user=user, id=doc_id)
        doc.delete()
        # text_doc = TextDocument.objects.delete(user=user, id=text_id)
    except PDFDocument.DoesNotExist:
        return HttpResponseRedirect(reverse("users:user-dashboard"))

    return HttpResponseRedirect(reverse("users:user-dashboard"))
