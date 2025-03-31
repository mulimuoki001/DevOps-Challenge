from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from .Forms.classes_form import ClassesForm
from .Forms.custom_user import CustomUserCreationForm
from .models import Booking, CustomUser, FitnessClasses


def is_admin(user):
    return user.is_staff


@login_required
def add_class(request):
    if request.method == "POST":
        form = ClassesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class added successfully")
            return redirect("fitness_booking_app:index")
        else:
            messages.error(request, "Please fill all the fields")
    else:
        form = ClassesForm()
    return render(request, "fitness_booking_app/add_class.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            username = form.cleaned_data.get("username")
            if CustomUser.objects.filter(username=username).exists():
                raise ValidationError("Username already exists")
            else:
                messages.success(request, f"Account created for {username}")
                return redirect(reverse("registration/login.html"))
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("fitness_booking_app:login")


@login_required
def index(request):
    # Always fetch fitness classes for display
    fitness_classes = FitnessClasses.objects.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            fitness_class_id = request.POST.get("fitness_class_id")

            try:
                fitness_class = FitnessClasses.objects.get(id=fitness_class_id)
            except FitnessClasses.DoesNotExist:
                messages.error(request, "Selected class does not exist.")
                return redirect("fitness_booking_app:index")

            if fitness_class.capacity > 0:
                fitness_class.capacity -= 1
                fitness_class.save()

                Booking.objects.create(user=request.user, fitness_class=fitness_class)

                messages.success(request, "Class booked successfully")
            else:
                messages.error(request, "Class is full")

        else:
            messages.error(request, "You are not logged in")
            return redirect("login")

        return redirect("fitness_booking_app:index")

    return render(
        request, "fitness_booking_app/index.html", {"fitness_classes": fitness_classes}
    )


@login_required
def book_class(request, fitness_class_id):
    fitness_class = FitnessClasses.objects.get(id=fitness_class_id)
    if fitness_class.capacity == 0:
        messages.error(request, "Class is full")
        return redirect("fitness_classes")
    elif Booking.objects.filter(
        user=request.user, fitness_class=fitness_class
    ).exists():
        messages.error(request, "You have already booked this class")
        return redirect("fitness_booking_app:index")
    else:
        booking_date = fitness_class.date
        booking_start_time = datetime.combine(booking_date, fitness_class.start_time)
        booking_end_time = datetime.combine(booking_date, fitness_class.end_time)

        Booking.objects.create(
            user=request.user,
            fitness_class=fitness_class,
            start_time=booking_start_time,
            end_time=booking_end_time,
        )
        fitness_class.capacity -= 1
        fitness_class.save()
        messages.success(request, "Class booked successfully")
        return render(
            request, "fitness_booking_app/index.html", {"fitness_class": fitness_class}
        )


@login_required
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "fitness_booking_app/bookings.html", {"bookings": bookings})
