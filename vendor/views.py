from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from accounts.decorators import role_required
from accounts.models import User
from .forms import MenuItemForm, OpeningHoursFormSet
from .models import MenuItem, OpeningHours
# Create your views here.


@role_required(User.Role.VENDOR)
def vendor_dashboard(request):
    return render(request, 'vendor/vendor_dashboard.html')

@login_required
@role_required(User.Role.VENDOR)
def vendor_settings(request):
    vendor_profile = request.user.vendorprofile
    return render(request, 'vendor/settings.html', {
        'vendor_profile': vendor_profile,
    })

@role_required(User.Role.VENDOR)
def vendor_menu(request):
    vendor_profile = request.user.vendorprofile
    menu_items = MenuItem.objects.filter(
        vendor=vendor_profile
    )
    items_count = menu_items.count()
    business_name = vendor_profile.business_name
    context = {
        'menu_items': menu_items,
        'business_name': business_name,
        'items_count': items_count
    }
    return render(request, 'vendor/vendor_menu.html', context)



@role_required(User.Role.VENDOR)
def add_menu_item(request):
    vendor_profile = request.user.vendorprofile

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, vendor_profile=vendor_profile)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.vendor = vendor_profile
            menu_item.save()
            return redirect('vendor:vendor_menu')

    else:
        form = MenuItemForm(vendor_profile=vendor_profile)

    return render(request, 'vendor/add_menu_item.html', {
        'form': form
    })



@role_required(User.Role.VENDOR)
def edit_menu_item(request, item_id):
    vendor_profile = request.user.vendorprofile
    menu_item = get_object_or_404(MenuItem, id=item_id, vendor=vendor_profile)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item, vendor_profile=vendor_profile)
        if form.is_valid():
            form.save()
            return redirect('vendor:vendor_menu')

    else:
        form = MenuItemForm(vendor_profile=vendor_profile, instance=menu_item)

    return render(request, 'vendor/edit_menu_item.html', {
        'form': form,
        'menu_item': menu_item
    })


@require_POST
@role_required(User.Role.VENDOR)
def delete_menu_item(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, vendor=request.user.vendorprofile)
    menu_item.delete()
    return redirect('vendor:vendor_menu')


@require_POST
@role_required(User.Role.VENDOR)
def toggle_item_availability(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, vendor=request.user.vendorprofile)
    menu_item.is_available = not menu_item.is_available
    menu_item.save()
    return redirect('vendor:vendor_menu')




@role_required(User.Role.VENDOR)
def vendor_opening_hours(request):
    vendor_profile = request.user.vendorprofile
    queryset = OpeningHours.objects.filter(vendor=vendor_profile)

    if request.method == 'POST':
        formset = OpeningHoursFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect('vendor:vendor_settings')
    else:
        formset = OpeningHoursFormSet(queryset=queryset)

    return render(request, 'vendor/opening_hours.html', {'formset': formset})