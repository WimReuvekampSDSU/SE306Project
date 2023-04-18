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
]