# printshop/admin.py

from django.contrib import admin

from .models import Category, Product, FilamentDetails, Customer, Order, OrderItem

admin.site.site_header = "FDMShop Administration"
admin.site.site_title="FDMShop Admin"
admin.site.index_title="Welcome to the FDMShop Admin Panel"


# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock_quantity', 'brand', 'created_at')
    search_fields = ('name', 'brand')
    list_filter = ('category', 'brand')
    ordering = ('-created_at',)

    # Define fieldsets for the Product model (for the form view)
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'brand', 'price', 'stock_quantity')  # Basic fields
        }),
        ('Advanced Information', {
            'classes': ('collapse',),  # This will make it collapsible
            'fields': ('description',)  # Don't include created_at here since it's non-editable
        })
    )
# Register FilamentDetails model
@admin.register(FilamentDetails)
class FilamentDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'material', 'color', 'diameter', 'weight')
    search_fields = ('product__name', 'material', 'color')
    list_filter = ('material', 'color')

# Register Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'total_price', 'status')
    search_fields = ('customer__name', 'status')
    list_filter = ('status',)
    ordering = ('-order_date',)

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__status', 'product__category')
    ordering = ('order',)