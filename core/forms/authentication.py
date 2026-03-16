from django import forms
from django.contrib.auth import authenticate


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
