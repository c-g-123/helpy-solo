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

    class Meta:
        model = User
        fields = ["email",]
        widgets = {"name": forms.EmailInput(attrs={"placeholder": "Email",}),}


class UsernameForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username",]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Username", }), }
