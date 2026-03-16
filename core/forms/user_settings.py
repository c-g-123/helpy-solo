from django import forms
from django.contrib.auth.models import User
from core.models import UserSettings


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
