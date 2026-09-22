from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404
from accounts.decorators import role_required
from accounts.models import User
from .forms import MenuItemForm, OpeningHoursFormSet, MenuItemVariantForm
from .models import MenuItem, OpeningHours, MenuItemVariant
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
    ).prefetch_related(
        'variants'
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
def menu_item_variant(request, item_id, variant_id=None):
    menu_item = get_object_or_404(MenuItem.objects.prefetch_related(
        'variants'
    ), id=item_id, vendor=request.user.vendorprofile)
    menu_item_variants = menu_item.variants.all()

    variant_forms = [MenuItemVariantForm(instance=v) for v in menu_item_variants]
    add_form = MenuItemVariantForm()

    context = {
        'menu_item': menu_item,
        'menu_item_variants': menu_item_variants,
        'add_form': add_form
    }

    if request.method == 'POST':
        if variant_id:
            item_variant = get_object_or_404(MenuItemVariant, id=variant_id, menu_item=menu_item)
            form = MenuItemVariantForm(request.POST, instance=item_variant)
            variant_forms = []
            for variant in menu_item_variants:
                if variant.pk == item_variant.pk:
                    variant_forms.append(form)
                else:
                    variant_forms.append(MenuItemVariantForm(instance=variant))
            if form.is_valid():
                form.save()
                return redirect('vendor:variants', item_id=item_id)
            context['form'] = form
            context['variant_forms'] = variant_forms
            return render(request, 'vendor/variants.html', context)

        form = MenuItemVariantForm(request.POST)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.menu_item = menu_item
            variant.save()
            return redirect('vendor:variants', item_id=item_id)
        context['variant_forms'] = variant_forms
        context['add_form'] = form
        return render(request, 'vendor/variants.html', context)

    context['variant_forms'] = variant_forms
    return render(request, 'vendor/variants.html', context)



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