from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect


def home_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:user-dashboard"))

    return render(request, "index.html")
