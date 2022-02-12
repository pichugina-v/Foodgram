from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'username',
        'email'
    )
    list_filter = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author'
    )
    search_fields = ('user', 'author')
