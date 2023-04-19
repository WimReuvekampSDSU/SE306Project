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

from .models import Item, Category, Review

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'image', 'category', 'quantity']

    def save(self, user=None, commit=True):
        item = super().save(commit=False)
        if user:
            item.seller = user
        if commit:
            item.save()
        return item


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(max_length=100, label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }