from django.shortcuts import render
from .forms import PDFDocumentForm

# Create your views here.


def document_upload(request):
    form = PDFDocumentForm()

    if request.method == "POST":
        form = PDFDocumentForm(request.POST, request.FILES)
        print(request.FILES)

    context = {"form": form}
    return render(request, "documents/upload.html", context=context)
