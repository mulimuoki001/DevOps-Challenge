from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


# CustomUser class/model
class CustomUser(AbstractUser):
    phone_number = (models.CharField(max_length=15, unique=True),)
    membership_type = (
        models.CharField(
            max_length=15,
            choices=(("GOLD", "GOLD"), ("SILVER", "SILVER"), ("BRONZE", "BRONZE")),
            default="BRONZE",
        ),
    )
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

    def __str__(self):
        return self.username


# Fitness Class model
class FitnessClass(models.Model):
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
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    date = models.DateField()
    booked_at = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return (
            f"{self.user.username} booked {self.fitness_class.name} on {self.booked_at}"
        )
