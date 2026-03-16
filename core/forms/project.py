from django import forms
from core.models import Project


class ProjectForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Name"
        })
    )

    class Meta:
        model = Project
        fields = [
            "name",
        ]
