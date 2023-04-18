from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('browse/', views.browse_listings, name='browse'),
    path('logout/', views.logout_view, name='logout'),
]