from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'first_name',
        'last_name', 'username', 'email'
    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'
