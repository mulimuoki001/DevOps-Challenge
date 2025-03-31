from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Booking, FitnessClasses


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            if User.objects.filter(username=username).exists():
                raise ValidationError("Username already exists")
            else:
                messages.success(request, f"Account created for {username}")
                return redirect(reverse("registration/login.html"))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("fitness_booking_app:login")


@login_required
def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            fitness_class_id = request.POST.get("fitness_class_id")
            fitness_class = FitnessClasses.objects.get(id=fitness_class_id)
            if fitness_class.capacity > 0:
                Booking.objects.create(
                    user=request.user,
                    fitness_class=fitness_class,
                    date=fitness_class.date,
                    start_time=fitness_class.start_time,
                    end_time=fitness_class.end_time,
                )
                fitness_class.capacity -= 1
                fitness_class.save()
                messages.success(request, "Class booked successfully")
                return redirect("index")
            else:
                messages.error(request, "Class is full")
                return redirect("index")
        else:
            messages.error(request, "You are not logged in")
            return redirect("login")
    return render(request, "fitness_booking_app/index.html")


@login_required
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "fitness_booking_app/bookings.html", {"bookings": bookings})
