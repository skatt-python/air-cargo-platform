from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'company_name', 'user_type', 'is_premium', 'rating', 'is_active')
    list_filter = ('user_type', 'is_premium', 'is_active')
    search_fields = ('email', 'company_name', 'phone')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Информация о компании', {'fields': ('company_name', 'phone', 'user_type')}),
        ('Рейтинг и статистика', {'fields': ('rating', 'total_ratings')}),
        ('Подписка', {'fields': ('is_premium',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'company_name', 'phone', 'user_type'),
        }),
    )


admin.site.register(User, CustomUserAdmin)