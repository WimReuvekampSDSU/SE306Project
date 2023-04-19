from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Item
import random
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.views.decorators.http import require_http_methods

#User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            authenticated_user = authenticate(username=username, password=password)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def homepage(request):
    return render(request, 'homepage.html')

def browse_listings(request):
    items = Item.objects.all()
    random_items = random.sample(list(items), min(len(items), 8))
    context = {'items': random_items}
    return render(request, 'browse_listings.html', context)

from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')  # or wherever you want to redirect the user
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')

from django.contrib.auth.decorators import login_required
from .forms import ItemForm

@login_required
def list_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'list_item.html', {'form': form})


from .models import Category
from .forms import CategoryForm
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_item')  # redirect to the 'add_item' view
    else:
        form = CategoryForm()
    return render(request, 'category_list.html', {'form': form})

@login_required
def category_list(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    context = {'categories': categories, 'form': form}
    return render(request, 'category_list.html', context)

def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')

from .models import Item

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_detail.html', {'item': item})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f'New message from {name}'
            message = f'From: {email}\n\n{message}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_EMAIL]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Thank you for your message. We will be in touch shortly.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})