import datetime
from django import forms
from absenceCalendar.models import Absence
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = 'date'


class AbsenceForm(ModelForm):
    class Meta:
        model = Absence
        fields = ['absenceFrom', 'absenceTo']
        widgets = {
            'absenceFrom': DateInput,
            'absenceTo': DateInput
        }

    def clean(self):
        today = datetime.date.today()
        start_date = self.cleaned_data.get("absenceFrom")
        end_date = self.cleaned_data.get("absenceTo")

        if end_date < start_date:
            raise forms.ValidationError("end date should be greater than start date")
        if end_date < today:
            raise forms.ValidationError("end date should be in the future or at least be today")
        if start_date < today:
            raise forms.ValidationError("start date should be at least be today")
