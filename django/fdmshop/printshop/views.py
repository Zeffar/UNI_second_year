from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Product, Category, FilamentDetails, Basket, BasketItem
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import FilamentFilterForm, ContactForm, ProductForm, RegistrationForm, LoginForm
from django.conf import settings
import json
from django.shortcuts import get_object_or_404, redirect
import os
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from time import time
from django.urls import get_resolver, reverse

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

def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Save with both product and filament details
            return redirect('.')  # Adjust to your desired redirection
    else:
        form = ProductForm()

    return render(request, 'printshop/add_product.html', {'form': form}) 

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'printshop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            remember_me = form.cleaned_data.get('remember_me')
            if remember_me:
                request.session.set_expiry(86400)  # 1 day in seconds
            else:
                request.session.set_expiry(0)  # Session expires on browser close
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'printshop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    user_data = {
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
        'address': user.address,
        'profile_picture': user.profile_picture.url if user.profile_picture else None,  # URL for profile picture
        'bio': user.bio,
    }

    print("Profile Picture URL:", user_data['profile_picture'])  # Debugging

    # Store user data in session
    request.session['user_data'] = user_data

    return render(request, 'printshop/profile.html', {'user_data': user_data})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'printshop/change_password.html'
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        print("Redirecting to:", self.success_url)  # Debugging log
        return self.success_url

change_password_view = login_required(CustomPasswordChangeView.as_view())



def index_view(request):
    """
    Render a template displaying all available URLs (excluding admin URLs) as clickable links.
    """
    url_patterns = get_resolver().url_patterns
    urls = []

    def extract_urls(patterns, prefix=""):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):  # For included URL patterns
                extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                # Skip admin URLs
                if not str(pattern.pattern).startswith("admin"):
                    url_name = getattr(pattern, 'name', None)
                    if url_name:  # Only include named URLs
                        try:
                            urls.append({'name': url_name, 'url': reverse(url_name)})
                        except Exception:
                            pass  # Skip if reverse fails

    extract_urls(url_patterns)
    return render(request, 'printshop/index.html', {'urls': urls})

from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Basket, BasketItem, Product

# Add item to basket
def add_to_basket(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        # Ensure stock is available
        if product.stock_quantity <= 0:
            # messages.warning(request, f"{product.name} is out of stock.")
            return redirect('product_filter')

        # Get or create the user's basket
        basket, created = Basket.objects.get_or_create(user=request.user)

        # Get or create the basket item
        basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

        # Update quantity
        if basket_item.quantity < product.stock_quantity:
            if not created:
                basket_item.quantity += 1
            basket_item.save()

            product.stock_quantity -= 1
            product.save()

        #     messages.success(request, f"Added {product.name} to your basket.")
        # else:
        #     messages.warning(request, f"Cannot add more {product.name}, stock limit reached.")

        return redirect('virtual_basket')
    return HttpResponseBadRequest("Invalid request method.")

# Update item quantity in basket
def update_quantity(request, item_id):
    if request.method == 'POST':
        basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
        quantity = int(request.POST.get('quantity', basket_item.quantity))
        
        if 0 < quantity <= basket_item.product.stock_quantity:
            basket_item.product.stock_quantity = basket_item.product.stock_quantity - quantity + basket_item.quantity
            basket_item.product.save()

            basket_item.quantity = quantity
            basket_item.save()

            
            messages.success(request, f"Updated {basket_item.product.name} quantity to {quantity}.")
        else:
            messages.error(request, f"Invalid quantity for {basket_item.product.name}.")
        return redirect('virtual_basket')
    return HttpResponseBadRequest("Invalid request method.")

# Remove item from basket
def remove_from_basket(request, item_id):
    basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    basket_item.product.stock_quantity += basket_item.quantity
    basket_item.product.save()

    basket_item.delete()
    messages.success(request, "Item removed from your basket.")
    return redirect('virtual_basket')

# Increment item quantity
def increment_quantity(request, item_id):
    basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    if basket_item.quantity < basket_item.product.stock_quantity:
        basket_item.quantity += 1
        basket_item.save()

        basket_item.product.stock_quantity -= 1
        basket_item.product.save()

        messages.success(request, f"Incremented {basket_item.product.name} quantity.")
    else:
        messages.warning(request, f"Cannot add more {basket_item.product.name}, stock limit reached.")
    return redirect('virtual_basket')

# Decrement item quantity
def decrement_quantity(request, item_id):
    basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    if basket_item.quantity > 1:
        basket_item.quantity -= 1
        basket_item.save()

        basket_item.product.stock_quantity += 1
        basket_item.product.save()
        
        messages.success(request, f"Decremented {basket_item.product.name} quantity.")
    else:
        messages.warning(request, f"Minimum quantity for {basket_item.product.name} is 1.")
    return redirect('virtual_basket')

# Virtual basket view
def virtual_basket_view(request):
    basket = Basket.objects.filter(user=request.user).first()
    if not basket:
        return render(request, 'printshop/virtual_basket.html', {
            'items': [],
            'total_price': 0,
            'total_items': 0,
        })

    items = basket.items.all()
    total_price = sum(item.product.price * item.quantity for item in items)
    total_items = sum(item.quantity for item in items)

    return render(request, 'printshop/virtual_basket.html', {
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
    })
