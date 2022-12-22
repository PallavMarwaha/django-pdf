from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import PDFDocumentForm
import PyPDF2
from .models import TextDocument, PDFDocument
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
# def pdf_to_text(pdf_doc):
#     with open(pdf_doc, "rb") as file:
#         # Read the file
#         pdf = PyPDF2.PdfFileReader(file)
#         content = ""

#         for ii in range(pdf.getNumPages()):
#             # Get the page
#             page = pdf.getPage(ii)
#             content += page.extract_text()

#         return content


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


def document_upload(request):

    if request.method == "POST":
        form = PDFDocumentForm(request.POST, request.FILES, user=request.user)
        # print(request.FILES)
        # form.is_valid()
        # print(form.errors)

        if form.is_valid():
            pdf_doc = request.FILES["document"]

            print(pdf_doc)

            # Create PDF object
            pdf_obj = PDFDocument.objects.create(user=request.user, document=pdf_doc)

            # Get the content from the PDF document
            content = pdf_to_text(pdf_doc=pdf_doc)

            # Create a TextDocument model
            TextDocument.objects.create(
                user=request.user, pdf=pdf_obj, title=pdf_doc.name, body=content
            )

            return HttpResponseRedirect(reverse("users:user-dashboard"))

    form = PDFDocumentForm()
    context = {"form": form}
    return render(request, "documents/upload.html", context=context)
