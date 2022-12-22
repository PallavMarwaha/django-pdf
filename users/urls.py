from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.user_login, name="user-login"),
    path("signup/", views.user_signup, name="user-signup"),
]
