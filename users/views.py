from django.shortcuts import render
from .forms import UserLoginForm, UserSignUpForm
from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()
# Create your views here.


def user_login(request):
    """
    Renders and authenticates user login
    """

    if request.method == "POST":

        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)

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


def user_logout(request):
    logout(request=request)
