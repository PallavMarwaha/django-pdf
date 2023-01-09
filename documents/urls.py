from django.urls import path, include
from .views import document_upload, text_detail_View, document_serve, document_delete

app_name = "documents"

urlpatterns = [
    path("upload/", document_upload, name="document-upload"),
    path("detail/<int:text_id>", text_detail_View, name="detail-view"),
    path("detail/<int:text_id>/download", document_serve, name="document-serve"),
    path("delete/<int:doc_id>", document_delete, name="document-delete"),
]
