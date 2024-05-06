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


class LoginForm(forms.Form):
    """
    Custom Login Form.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    """
    Custom Profile Form.
    """
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(
            datetime.date.today().year - 100,
            datetime.date.today().year + 1
        )
        )
    )

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'avatar']
