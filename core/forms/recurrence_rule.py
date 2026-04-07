from django import forms
from core.models.recurrence_rule import RecurrenceRule


class RecurrenceRuleForm(forms.ModelForm):

    class Meta:
        model = RecurrenceRule
        fields = [
            'interval',
            'frequency',
            'end_datetime',
        ]

        widgets = {
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local",}),
        }
