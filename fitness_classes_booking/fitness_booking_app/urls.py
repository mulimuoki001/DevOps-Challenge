from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name = "fitness_booking_app"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "accounts/login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("register", views.register, name="register"),
    path("booking", views.bookings, name="booking"),
    path("accounts/profile/", views.index, name="profile"),
    path("logout", views.custom_logout, name="logout"),
]
