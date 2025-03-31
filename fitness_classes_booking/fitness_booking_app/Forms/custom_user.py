from django.contrib.auth.forms import UserCreationForm
from fitness_booking_app.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
