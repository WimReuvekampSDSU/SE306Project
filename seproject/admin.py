from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Item
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Item)

class MyUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff')

admin.site.register(User, MyUserAdmin)
