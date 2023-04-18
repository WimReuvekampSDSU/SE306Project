from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = get_user_model() # use the custom User model
        fields = ('username', 'email', 'password1', 'password2')

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    pass