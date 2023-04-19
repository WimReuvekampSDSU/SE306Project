from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from .models import Item, PurchasedItem, Category, Review, UserCategoryPreference
from .forms import CategoryForm, ItemForm, LoginForm, ContactForm, SignUpForm, ReviewForm
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy


@login_required
def account(request):
    if request.method == 'POST':
        # Update user info
        request.user.username = request.POST['username']
        request.user.email = request.POST['email']
        request.user.save()

        # Change password
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        # Display current user info
        form = PasswordChangeForm(user=request.user)

    return render(request, 'account.html', {'form': form, 'user': request.user})

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
    try:
        if request.user.is_authenticated:
            recommended = recommended_items(request.user)
            context = {'recommended_items': recommended}
            return render(request, "authenticated_homepage.html", context)
    except Exception as e:
            context = {'error_message': str(e)}
            if request.user.is_authenticated:
                return render(request, 'authenticated_homepage.html', context=None)
            else:
                return render(request, 'homepage.html')

    return render(request, 'homepage.html')


def browse_listings(request):
    try:
        items = Item.objects.all()
        random_items = random.sample(list(items), min(len(items), 8))
        context = {'items': random_items, 'recommended_items' : recommended_items(request.user)}
        return render(request, 'browse_listings.html', context)
    except Exception as a:
        context = {'error_message': str(a)}
        items = Item.objects.all()
        random_items = random.sample(list(items), min(len(items), 8))
        context = {'items': random_items}
        return render(request, 'browse_listings.html', context)
        

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

@login_required(login_url=reverse_lazy('login'))
def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)
    reviews = Review.objects.filter(item=item)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'item_detail.html', {'item': item, 'reviews': reviews, 'avg_rating': avg_rating})

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

def my_items(request):
    user = request.user
    items = Item.objects.filter(seller=user)
    context = {
        'items': items
    }
    return render(request, 'my_items.html', context)

@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    ItemForm = modelform_factory(Item, exclude=[])
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', pk=pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'edit_item.html', {'form': form})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('my_items')
    context = {'item': item}
    return render(request, 'delete_item.html', context)

@login_required
def purchase_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.quantity > 0:
        # Reduce the item quantity by 1
        item.quantity -= 1
        item.save()
        messages.success(request, f"You have successfully purchased {item.title}.")
        PurchasedItem.objects.create(item=item, buyer=request.user)
        update_user_category_preferences(request.user)
        return render(request, 'purchase_confirmation.html', {'item': item})
    else:
        messages.warning(request, f"{item.title} is out of stock.")
        return redirect('item_detail', pk=item.pk)

@login_required
def purchase_history(request):
    purchased_items = PurchasedItem.objects.filter(buyer=request.user)
    context = {'purchased_items': purchased_items}
    return render(request, 'purchase_history.html', context)

@login_required
def review_item(request, purchase_id):
    purchase = get_object_or_404(PurchasedItem, pk=purchase_id, buyer=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = purchase.item
            review.buyer = request.user
            review.save()
            messages.success(request, 'Your review has been posted.')
            return redirect('purchase_history')
    else:
        form = ReviewForm()
    return render(request, 'review_item.html', {'form': form, 'item': purchase.item})

def update_user_category_preferences(user):
    purchased_items = PurchasedItem.objects.filter(buyer=user)
    user_category_preferences = UserCategoryPreference.objects.filter(user=user)
    category_counts = {}

    # Count occurrences of each category in the user's purchased items
    for purchased_item in purchased_items:
        category = purchased_item.item.category
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    # Update the occurrence counts in the UserCategoryPreference model
    for user_category_preference in user_category_preferences:
        category = user_category_preference.category
        if category in category_counts:
            user_category_preference.occurrence_count = category_counts[category]
            user_category_preference.save()
            del category_counts[category]
        else:
            user_category_preference.occurrence_count = 0
            user_category_preference.save()

    # Create new entries for any remaining categories
    for category, count in category_counts.items():
        UserCategoryPreference.objects.create(
            user=user,
            category=category,
            occurrence_count=count
        )

def recommended_items(user):
    if not user.is_authenticated:
        items = Item.objects.all()
        recommended_items = []
        recommended_items = random.sample(list(items), min(len(items), 4))
        return recommended_items
    user_category_preferences = UserCategoryPreference.objects.filter(user=user).exclude(occurrence_count=0)
    total_occurrences = sum([preference.occurrence_count for preference in user_category_preferences])
    
    if total_occurrences == 0:
        items = Item.objects.all()
        recommended_items = []
        recommended_items = random.sample(list(items), min(len(items), 4))
        return recommended_items

    # Create a list of categories and their corresponding probabilities based on the user's preferences
    category_probabilities = []
    for preference in user_category_preferences:
        category_probabilities.append((preference.category, preference.occurrence_count / total_occurrences))
    
    # Choose up to 4 items, ensuring no duplicates
    recommended_items = []
    while len(recommended_items) < 4:
        # Choose a random category based on the category probabilities
        chosen_category = random.choices([cp[0] for cp in category_probabilities], [cp[1] for cp in category_probabilities])[0]
        
        # Choose a random item from the chosen category that hasn't already been recommended
        items_in_category = Item.objects.filter(category=chosen_category).exclude(id__in=[item.id for item in recommended_items])
        if items_in_category:
            recommended_items.append(random.choice(items_in_category))
        else:
            # If there are no items in the chosen category that haven't been recommended, remove that category from the list of choices
            category_probabilities = [cp for cp in category_probabilities if cp[0] != chosen_category]
            if not category_probabilities:
                # If there are no more categories to choose from, exit the loop
                break
    
    return recommended_items

