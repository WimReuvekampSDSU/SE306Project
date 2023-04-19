from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('browse/', views.browse_listings, name='browse'),
    path('logout/', views.logout_view, name='logout'),
    path('list_item/', views.list_item, name='list_item'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_list/', views.category_list, name='category_list'),
    path('category_delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('contact/', views.contact, name='contact'),
    path('my_items/', views.my_items, name='my_items'),
    path('items/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('my_items/delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('buy/<int:pk>/', views.purchase_item, name='buy-item'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
]