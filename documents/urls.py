from django.urls import path, include
from .views import document_upload

app_name = "documents"

urlpatterns = [path("upload/", document_upload, name="document-upload")]
