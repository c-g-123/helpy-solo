from django import forms
from core.models import Project, Task


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            "name",
        ]


class TaskForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Name"
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Description"
        })
    )

    set_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Task
        fields = [
            "project_id",
            "name",
            "description",
            "set_date",
            "due_date",
        ]
