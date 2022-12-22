from django import forms
from .models import PDFDocument
from django.contrib.auth import get_user_model

User = get_user_model()


class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ["document"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(PDFDocumentForm, self).__init__(*args, **kwargs)


# class PDFDocumentForm(forms.Form):
#     user = forms.ModelChoiceField(queryset=User.objects.all())
#     document = forms.FileField()
