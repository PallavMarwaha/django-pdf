from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserSignUpForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required

User = get_user_model()
# Create your views here.


def user_login(request):
    """
    Renders and authenticates user login
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:user-dashboard"))

    if request.method == "POST":

        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                return render(request, "users/dashboard.html")

    return render(request, "users/login.html")


def user_signup(request):
    """
    Renders and creates a new user
    """
    if request.method == "POST":

        form = UserSignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Check if the user does not already exist and create new user
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password)

    return render(request, "users/signup.html")


@login_required(login_url="users:user-login")
def user_logout(request):
    logout(request=request)
    return HttpResponseRedirect(reverse("home-page"))


@login_required(login_url="users:user-login")
def user_dashboard(request):
    """
    Renders user dashboard
    """
    return render(request, "users/dashboard.html")
