import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile


class SignupForm(UserCreationForm):
    """
    Custom Signup Form that extends the UserCreationForm.
    """

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        )
    )


class LoginForm(forms.Form):
    """
    Custom Login Form.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )


class ProfileForm(forms.ModelForm):
    """
    Custom Profile Form.
    """

    class Meta:
        model = Profile
        fields = ["bio", "location", "birth_date", "avatar"]

    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Bio",
            }
        )
    )

    location = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Location",
            }
        )
    )

    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(datetime.date.today().year - 100, datetime.date.today().year + 1),
            attrs={
                "class": "form-control",
            },
        ),
    )

    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        )
    )
