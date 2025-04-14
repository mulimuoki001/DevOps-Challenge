# CustomUser class/model
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


# CustomUser class/model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    MEMBERSHIP_CHOICES = (
        ("GOLD", "GOLD"),
        ("SILVER", "SILVER"),
        ("BRONZE", "BRONZE"),
    )
    membership_type = models.CharField(
        max_length=15,
        choices=MEMBERSHIP_CHOICES,
        default="BRONZE",
    )

    # Ensure username field is still functioning correctly
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    # Adjust related_name to avoid conflict
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Adjust related_name to avoid conflict
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Adjust related_name to avoid conflict
        blank=True,
        help_text=_("Specific permissions for this user."),
    )

    def __str__(self):
        return self.username


# Fitness Class model
class FitnessClasses(models.Model):
    class_name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    instructor_name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.class_name} - {self.date.strftime('%Y-%m-%d')} {self.start_time.strftime('%H:%M')}"


# Booking model
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(
        FitnessClasses, on_delete=models.CASCADE, related_name="bookings"
    )
    date = models.DateField(default=date.today)
    booked_at = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} booked {self.fitness_class.class_name} on {self.booked_at}"

    def save(self, *args, **kwargs):
        if self.fitness_class.bookings.count() >= self.fitness_class.capacity:
            raise ValidationError("Class is full")
        super().save(*args, **kwargs)
