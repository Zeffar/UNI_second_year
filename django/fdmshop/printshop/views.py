from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category, FilamentDetails
from django.http import JsonResponse
from .forms import FilamentFilterForm, ContactForm
from django.conf import settings
import json
import os
from time import time

def product_filter_view(request):
    # Get the Filaments category
    filaments_category = Category.objects.get(name="Filaments")

    # Instantiate the filter form
    form = FilamentFilterForm(request.GET)

    # Base queryset for filaments
    filaments = Product.objects.filter(category=filaments_category)

    if form.is_valid():  # Apply filters if the form is valid
        material = form.cleaned_data.get('material')
        color = form.cleaned_data.get('color')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        stock_min = form.cleaned_data.get('stock_min')
        stock_max = form.cleaned_data.get('stock_max')
        brand = form.cleaned_data.get('brand')
        diameter = form.cleaned_data.get('diameter')
        weight = form.cleaned_data.get('weight')

        # Apply product-level filters
        if min_price is not None:
            filaments = filaments.filter(price__gte=min_price)
        if max_price is not None:
            filaments = filaments.filter(price__lte=max_price)
        if stock_min is not None:
            filaments = filaments.filter(stock_quantity__gte=stock_min)
        if stock_max is not None:
            filaments = filaments.filter(stock_quantity__lte=stock_max)
        if brand:
            filaments = filaments.filter(brand__icontains=brand)

        # Join with FilamentDetails for filament-specific filters
        filament_details = FilamentDetails.objects.filter(product_id__in=filaments)

        if material:
            filament_details = filament_details.filter(material__iexact=material)
        if color:
            filament_details = filament_details.filter(color__icontains=color)
        if diameter is not None:
            filament_details = filament_details.filter(diameter=diameter)
        if weight is not None:
            filament_details = filament_details.filter(weight=weight)

        # Filter final products based on FilamentDetails
        filaments = filaments.filter(id__in=filament_details.values('product_id'))

    # Apply pagination: 8 items per page
    paginator = Paginator(filaments, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        results = [
            {
                'name': filament.name,
                'price': filament.price,
                'stock_quantity': filament.stock_quantity,
                'brand': filament.brand,
                'material': getattr(filament.filamentdetails, 'material', 'N/A'),
                'color': getattr(filament.filamentdetails, 'color', 'N/A'),
                'diameter': getattr(filament.filamentdetails, 'diameter', 'N/A'),
                'weight': getattr(filament.filamentdetails, 'weight', 'N/A'),
            }
            for filament in page_obj
        ]
        return JsonResponse({'results': results, 'page': page_obj.number, 'pages': paginator.num_pages})

    # Render template for standard GET requests
    return render(request, 'printshop/filaments.html', {'form': form, 'page_obj': page_obj})

def filaments_view(request):
    # Get the Filaments category
    filaments_category = Category.objects.get(name="Filaments")

    # Get filter parameters from the request
    material = request.GET.get('material', None)
    color = request.GET.get('color', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    stock_min = request.GET.get('stock_min', None)
    stock_max = request.GET.get('stock_max', None)
    brand = request.GET.get('brand', None)
    diameter = request.GET.get('diameter', None)
    weight = request.GET.get('weight', None)

    # Start with the base queryset for filaments
    filaments = Product.objects.filter(category=filaments_category)

    # Apply product-level filters
    if min_price:
        filaments = filaments.filter(price__gte=min_price)
    if max_price:
        filaments = filaments.filter(price__lte=max_price)
    if stock_min:
        filaments = filaments.filter(stock_quantity__gte=stock_min)
    if stock_max:
        filaments = filaments.filter(stock_quantity__lte=stock_max)
    if brand:
        filaments = filaments.filter(brand__icontains=brand)

    # Join with FilamentDetails for filament-specific filters
    filament_details = FilamentDetails.objects.filter(product_id__in=filaments)

    if material:
        filament_details = filament_details.filter(material__iexact=material)
    if color:
        filament_details = filament_details.filter(color__icontains=color)
    if diameter:
        filament_details = filament_details.filter(diameter=diameter)
    if weight:
        filament_details = filament_details.filter(weight=weight)

    # Get the final list of filtered products
    filtered_filaments = filaments.filter(id__in=filament_details.values('product_id'))

    # Apply pagination: 37 items per page
    paginator = Paginator(filtered_filaments, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the paginated filaments to the template
    return render(request, 'printshop/filaments.html', {'page_obj': page_obj})
    
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Extract cleaned data
            cleaned_data = form.cleaned_data
            mesaj = cleaned_data.pop('mesaj')
            confirmare_email = cleaned_data.pop('confirmare_email')  # Exclude from saved data

            # Preprocess data
            today = date.today()
            data_nasterii = cleaned_data['data_nasterii']
            age_years = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
            age_months = today.month - data_nasterii.month + (12 if today.month < data_nasterii.month else 0)
            cleaned_data['varsta'] = f"{age_years} years and {age_months} months"

            # Normalize message
            mesaj = ' '.join(mesaj.replace('\n', ' ').split())
            cleaned_data['mesaj'] = mesaj

            # Convert date fields to strings
            cleaned_data['data_nasterii'] = cleaned_data['data_nasterii'].isoformat()

            # Save data as JSON
            mesaje_dir = os.path.join(settings.BASE_DIR, 'mesaje')
            os.makedirs(mesaje_dir, exist_ok=True)
            timestamp = int(time())
            file_name = f"mesaj_{timestamp}.json"
            file_path = os.path.join(mesaje_dir, file_name)
            with open(file_path, 'w') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
            print(f"Saving message to: {file_path}")

            return render(request, 'printshop/success.html', {'file_path': file_path})
        else: 
            print(f"Saving message to: nothing")
    else:
        form = ContactForm()

    return render(request, 'printshop/contact.html', {'form': form})