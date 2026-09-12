from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Invitation


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
            'email',
            'phone_number',
            'role',
        ),
    }),
)



@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = [
        'created_by', 'role', 'created_at'
    ]

    list_filter = [
        'role'
    ]

