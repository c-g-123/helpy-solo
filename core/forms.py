from django import forms
from core.models import Project, Task


class ProjectForm(forms.ModelForm):

    name = forms.CharField(
        max_length=Project._meta.get_field("name").max_length,
        widget=forms.TextInput(attrs={
            "placeholder": "Name"
        })
    )

    class Meta:
        model = Project
        fields = [
            "name",
        ]


class TaskForm(forms.ModelForm):

    name = forms.CharField(
        max_length=Task._meta.get_field("name").max_length,
        widget=forms.TextInput(attrs={
            "placeholder": "Name"
        })
    )

    description = forms.CharField(
        max_length=Task._meta.get_field("description").max_length,
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
            "project",
            "name",
            "description",
            "set_date",
            "due_date",
        ]
