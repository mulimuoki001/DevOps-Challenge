from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name = "fitness_booking_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("add-class", views.add_class, name="add-class"),
    path(
        "accounts/login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("register", views.register, name="register"),
    path("accounts/profile/", views.index, name="profile"),
    path("logout", views.custom_logout, name="logout"),
    path("book-class/<int:fitness_class_id>/", views.book_class, name="book_class"),
    path("bookings/", views.bookings, name="bookings"),
]
