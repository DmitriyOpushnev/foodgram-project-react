from django.contrib import admin

from core.texts import EMPTY_STRING
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    exclude = [
        'last_login', 'is_staff', 'date_joined',
        'groups', 'user_permissions',
    ]
    search_fields = ('username',)
    list_filter = ('first_name', 'email')
    empty_value_display = EMPTY_STRING
