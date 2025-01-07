from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Import settings to access AUTH_USER_MODEL



# Category model for product categories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"  


# Product model for all products (FDM printers, filaments, etc.)
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Filament details model (specific to filament products)
class FilamentDetails(models.Model):
    MATERIAL_CHOICES = [
        ('PLA', 'PLA'),
        ('PETG', 'PETG'),
        ('ABS', 'ABS'),
        ('TPU', 'TPU'),
        ('PET', 'PET'),
        ('PST', 'PST'),
        ('CF-Reinforced', 'CF-Reinforced'),
    ]

    product = models.OneToOneField(Product, max_length=40, on_delete=models.CASCADE, related_name='filament_details')
    material = models.CharField(max_length=30, choices=MATERIAL_CHOICES)
    color = models.CharField(max_length=50)
    diameter = models.DecimalField(max_digits=3, decimal_places=2, help_text="Diameter in mm (e.g., 1.75)")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in grams")

    def __str__(self):
        return f"{self.color} {self.material} ({self.diameter}mm)"
    
    class Meta:
        verbose_name = "Filament detail"
        verbose_name_plural = "Filament details"


# Customer model for storing customer information
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Order model for tracking customer orders
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.status}"


# OrderItem model for storing individual items in an order
class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "Order items"


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Enter your phone number.")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Enter your date of birth.")
    address = models.TextField(blank=True, null=True, help_text="Enter your address.")
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True, help_text="Tell us something about yourself.")
    code = models.CharField(max_length=100, blank=True, null=True)  # Random confirmation code
    blocat = models.BooleanField(default=False, help_text="Mark as blocked to prevent user login")


class Basket(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price