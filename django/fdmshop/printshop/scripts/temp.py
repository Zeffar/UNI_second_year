# fdmshop/printshop/scripts/temp.py

from django.utils import timezone
from printshop.models import Category, Product, FilamentDetails, OrderItem, Order, Customer
from datetime import datetime
from django.db import connection

def reset_sequence(table_name):
    """Reset the auto-increment sequence for the primary key of the table."""
    with connection.cursor() as cursor:
        cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;")

def run():
    # Delete data from all tables, in the correct order to avoid foreign key violations
    OrderItem.objects.all().delete()  # Delete order items first
    Order.objects.all().delete()      # Then delete orders
    FilamentDetails.objects.all().delete()  # Then delete filament details
    Product.objects.all().delete()    # Delete products
    Customer.objects.all().delete()  # Delete customers
    Category.objects.all().delete()  # Delete categories last
    reset_sequence('printshop_category')
    reset_sequence('printshop_product')
    reset_sequence('printshop_filamentdetails')
    reset_sequence('printshop_customer')
    reset_sequence('printshop_order')
    reset_sequence('printshop_orderitem')
    # Create categories
    filaments_category, _ = Category.objects.get_or_create(
        name="Filaments",
        description="Filaments in various materials and colors"
    )

    printers_category, _ = Category.objects.get_or_create(
        name="FDM Printers",
        description="Affordable and reliable 3D printers"
    )

    # Define filament types and colors
    filament_types = ['PLA', 'PETG', 'ABS', 'TPU', 'PET', 'PPS', 'CF-Reinforced']
    colors = ['White', 'Beige', 'Grey', 'Yellow', 'Orange', 'Red', 'Green', 'Forest Green', 'Pink', 'Purple', 'Blue']
    diameters = [1.75, 2.85]  # Common filament diameters
    weights = [100, 200, 500]  # Sample filament weights (grams)

    # Loop through filament combinations and create products
    for filament_type in filament_types:
        for color in colors:
            for diameter in diameters:
                for weight in weights:
                    # Create the filament product
                    product_name = f"{filament_type} Filament - {color}"
                    product_description = f"{diameter}mm {filament_type} filament, {color} color"
                    filament_product, _ = Product.objects.get_or_create(
                        name=product_name,
                        description=product_description,
                        price=20.00,  # Set a fixed price for simplicity
                        stock_quantity=50,
                        category=filaments_category,
                        brand="Generic",
                        created_at=timezone.now()
                    )
                    # Create filament details
                    FilamentDetails.objects.get_or_create(
                        product=filament_product,
                        material=filament_type,
                        color=color,
                        diameter=diameter,
                        weight=weight
                    )

    # Define printer products
    printer_data = [
        {"name": "Creality Ender 3 V2", "brand": "Creality", "price": 250.00, "stock_quantity": 10},
        {"name": "Prusa i3 MK3", "brand": "Prusa", "price": 750.00, "stock_quantity": 5},
        {"name": "Anycubic i3 Mega", "brand": "Anycubic", "price": 200.00, "stock_quantity": 20},
        {"name": "Artillery Sidewinder X1", "brand": "Artillery", "price": 400.00, "stock_quantity": 15},
    ]

    # Loop through printer data and create products
    for printer in printer_data:
        printer_product, _ = Product.objects.get_or_create(
            name=printer['name'],
            description=f"Reliable {printer['name']} 3D printer",
            price=printer['price'],
            stock_quantity=printer['stock_quantity'],
            category=printers_category,
            brand=printer['brand'],
            created_at=timezone.now()
        )

    print("Filament and Printer products created successfully!")

    