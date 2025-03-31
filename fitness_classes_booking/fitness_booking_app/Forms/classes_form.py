from django import forms
from fitness_booking_app.models import FitnessClasses


class ClassesForm(forms.ModelForm):
    class Meta:
        model = FitnessClasses
        fields = "__all__"

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }
