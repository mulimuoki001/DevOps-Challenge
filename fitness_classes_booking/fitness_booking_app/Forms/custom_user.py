from django.contrib.auth.forms import UserCreationForm
from fitness_booking_app.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        if CustomUser.objects.filter(username=username).exists():
            self.add_error("username", "Username already exists")
        return username

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["email"].widget.attrs["placeholder"] = "Email address"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone number"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm password"
