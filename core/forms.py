from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from core.models import Project, Task, UserSettings


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        user = authenticate(
            username=cleaned_data.get("username"),
            password=cleaned_data.get("password")
        )

        if not user:
            raise forms.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise forms.ValidationError("Your account is disabled.")

        cleaned_data["authenticated_user"] = user
        return cleaned_data


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

    set_datetime = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    due_datetime = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Task
        fields = [
            "project",
            "parent_task",
            "name",
            "description",
            "set_datetime",
            "due_datetime",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["project"].queryset = Project.objects.filter(user=user)
            self.fields["parent_task"].queryset = Task.objects.filter(project__user=user)
            self.fields["parent_task"].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get("project")
        parent_task = cleaned_data.get("parent_task")

        if parent_task and parent_task.project != project:
            raise forms.ValidationError("A subtask must belong to the same project as its parent task.")

        return cleaned_data

class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = UserSettings
        fields = [
            "theme",
            "default_page",
        ]


class UserEmailForm(forms.ModelForm):

    email = forms.EmailField(
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
        widget=forms.TextInput(attrs={
            "placeholder": "Username"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
        ]
