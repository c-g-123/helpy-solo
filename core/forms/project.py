from django import forms
from core.models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["name",]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Project name",}),}
