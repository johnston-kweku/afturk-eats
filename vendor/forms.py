from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import MenuItem, OpeningHours


INPUT_CLASSES = "outline-none border focus:ring-1 focus:ring-sand-100/30 border-sand-200/10 rounded-xl px-2 py-3 w-full placeholder:text-sand-100/30 text-sand-100 placeholder:text-sm caret-sand-100 placeholder:font-light bg-transparent"


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'category', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'e.g. Jollof Rice & Chicken',
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
                'rows': 4,
                'placeholder': 'Briefly describe the dish — ingredients, portion size, what makes it special...',
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'peer sr-only',
            }),
        }

    def __init__(self, *args, vendor_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        if vendor_profile:
            self.fields['category'].queryset = vendor_profile.category.all()



OpeningHoursFormSet = modelformset_factory(
    OpeningHours,
    fields=['open_time', 'close_time', 'is_closed'],
    extra=0,
    widgets={
        'open_time': forms.TimeInput(attrs={'class': INPUT_CLASSES, 'type': 'time'}),
        'close_time': forms.TimeInput(attrs={'class': INPUT_CLASSES, 'type': 'time'}),
        'is_closed': forms.CheckboxInput(attrs={'class': 'w-4 h-4 accent-cyprus-700'}),
    },
)