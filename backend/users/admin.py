from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """Просмотр моделей для модели User."""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_subscribed',
        'role',
    )
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'
    list_filter = ('username', 'email',)
    list_editable = (
        'first_name',
        'last_name',
        'is_subscribed',
        'role',
    )


admin.site.register(User, UserAdmin)
