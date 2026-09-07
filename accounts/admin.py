from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = [
        'username',
        'first_name',
        'last_name',
        'role',
        'public_id',
        'phone_number',
        'email',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
            ),
        }),
        ('Personal information', {
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'email',
                'phone_number',
            ),
        }),
        ('Afturk Eats', {
            'fields': (
                'role',
            ),
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Important dates', {
            'fields': (
                'last_login',
                'date_joined',
            ),
        }),
    )

    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': (
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'phone_number',
            'role',
        ),
    }),
)