from django import forms
from django.contrib.auth.models import User
from core.models import Project, Task, UserSettings


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["project"].queryset = Project.objects.filter(user=user)

class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = UserSettings
        fields = [
            "theme",
            "default_page",
        ]

class UserEmailForm(forms.ModelForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Email"
        })
    )

    class Meta:
        model = User
        fields = [
            "email",
        ]

class UsernameForm(forms.ModelForm):

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Username"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
        ]