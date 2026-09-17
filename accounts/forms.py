from django import forms
from .models import User, Invitation

INPUT_CLASSES = "outline-none border focus:ring-1 focus:ring-sand-100/30 border-sand-200/10 rounded-xl px-2 py-3 w-full placeholder:text-sand-100/30 text-sand-100 placeholder:text-sm caret-sand-100 placeholder:font-light bg-transparent"

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'your_username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Johnston'
            }),
            'last_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Mason'
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'valid_email@example.com'
            })
        }