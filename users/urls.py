from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.user_login, name="user-login"),
    path("signup/", views.user_signup, name="user-signup"),
    path("logout", views.user_logout, name="user-logout"),
    path("dashboard/", views.user_dashboard, name="user-dashboard"),
    path("documents/", include("documents.urls", namespace="documents")),
    
]
