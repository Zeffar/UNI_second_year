# FDMPrinter Django Project Documentation

## Project Overview
The FDMPrinter project is a Django-based web application designed to manage and showcase a variety of 3D printing products, including filaments and FDM printers. The project includes user authentication, product management, and a virtual basket for managing orders.

## Project Structure
The project is organized into several Django apps and modules, each responsible for different functionalities.

### Apps
1. **printshop**: This app handles the core functionalities of the project, including product management, user authentication, and order processing.

### Models
The project includes several models to represent different entities in the application:

1. **Category**: Represents product categories.
    - `name`: CharField, unique, max_length=100
    - `description`: TextField, optional
    - `__str__`: Returns the name of the category

2. **Product**: Represents products available in the shop.
    - `name`: CharField, max_length=255
    - `description`: TextField, optional
    - `price`: DecimalField, max_digits=10, decimal_places=2
    - `stock_quantity`: PositiveIntegerField, default=0
    - `category`: ForeignKey to Category, related_name='products'
    - `brand`: CharField, max_length=100, optional
    - `created_at`: DateTimeField, auto_now_add=True
    - `__str__`: Returns the name of the product

3. **FilamentDetails**: Stores specific details about filament products.
    - `product`: OneToOneField to Product, related_name='filament_details'
    - `material`: CharField, choices=[('PLA', 'PLA'), ('PETG', 'PETG'), ('ABS', 'ABS'), ('TPU', 'TPU'), ('PET', 'PET'), ('PST', 'PST'), ('CF-Reinforced', 'CF-Reinforced')]
    - `color`: CharField, max_length=50
    - `diameter`: DecimalField, max_digits=3, decimal_places=2, help_text="Diameter in mm (e.g., 1.75)"
    - `weight`: DecimalField, max_digits=5, decimal_places=2, help_text="Weight in grams"
    - `__str__`: Returns a string representation of the filament details

4. **Customer**: Stores customer information.
    - `name`: CharField, max_length=255
    - `email`: EmailField, unique
    - `phone`: CharField, max_length=20, optional
    - `address`: TextField
    - `created_at`: DateTimeField, auto_now_add=True
    - `__str__`: Returns the name of the customer

5. **Order**: Represents customer orders.
    - `customer`: ForeignKey to Customer, related_name='orders'
    - `order_date`: DateTimeField, auto_now_add=True
    - `total_price`: DecimalField, max_digits=10, decimal_places=2
    - `status`: CharField, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending'
    - `__str__`: Returns a string representation of the order

6. **OrderItem**: Represents individual items in an order.
    - `order`: ForeignKey to Order, related_name='order_items'
    - `product`: ForeignKey to Product, related_name='order_items'
    - `quantity`: PositiveIntegerField
    - `price`: DecimalField, max_digits=10, decimal_places=2
    - `__str__`: Returns a string representation of the order item

7. **CustomUser**: Extends the default Django user model with additional fields.
    - `phone_number`: CharField, max_length=15, optional
    - `date_of_birth`: DateField, optional
    - `address`: TextField, optional
    - `profile_picture`: ImageField, optional
    - `bio`: TextField, optional
    - `code`: CharField, max_length=100, optional
    - `blocat`: BooleanField, default=False, help_text="Mark as blocked to prevent user login"

8. **Basket**: Represents a user's shopping basket.
    - `user`: OneToOneField to CustomUser
    - `created_at`: DateTimeField, auto_now_add=True

9. **BasketItem**: Represents individual items in a user's basket.
    - `basket`: ForeignKey to Basket, related_name='items'
    - `product`: ForeignKey to Product
    - `quantity`: PositiveIntegerField, default=1
    - `subtotal`: Method to calculate the subtotal for the item

### Forms
The project includes several forms for user input and data validation:

1. **FilamentFilterForm**: Used for filtering filament products.
    - Fields: material, color, min_price, max_price, stock_min, stock_max, brand, diameter, weight

2. **ContactForm**: Used for submitting contact messages.
    - Fields: nume, prenume, data_nasterii, email, confirmare_email, tip_mesaj, subiect, minim_zile_asteptare, mesaj
    - Custom validation: Ensures email confirmation, validates user age, and checks that the message ends with the user's name

3. **ProductForm**: Used for adding new products.
    - Fields: name, price, quantity_to_add, user_initials, material, color, diameter, weight
    - Custom validation: Ensures valid price, quantity, and total value of stock

4. **RegistrationForm**: Used for user registration.
    - Fields: username, email, phone_number, date_of_birth, address, profile_picture, bio, password1, password2
    - Custom validation: Ensures user is at least 18 years old, phone number contains only digits, and bio contains at least 10 words

5. **LoginForm**: Used for user login.
    - Fields: username, password, remember_me

### Views
The project includes several views to handle different functionalities:

1. **product_filter_view**: Handles filtering and displaying filament products.
    - Retrieves filter parameters from the request and applies them to the queryset
    - Supports pagination and AJAX requests for dynamic updates

2. **filaments_view**: Displays a list of filament products.
    - Retrieves filter parameters from the request and applies them to the queryset
    - Supports pagination

3. **contact_view**: Handles contact form submissions.
    - Validates and processes the contact form
    - Saves the message as a JSON file

4. **add_product_view**: Handles adding new products.
    - Validates and saves the product form
    - Automatically sets the category to "Filaments"

5. **register_view**: Handles user registration.
    - Validates and saves the registration form
    - Logs in the user upon successful registration

6. **login_view**: Handles user login.
    - Validates and processes the login form
    - Supports "Remember Me" functionality

7. **logout_view**: Handles user logout.
    - Logs out the user and redirects to the login page

8. **profile_view**: Displays the user's profile.
    - Retrieves and displays user data
    - Stores user data in the session

9. **CustomPasswordChangeView**: Handles password change requests.
    - Customizes the password change view
    - Redirects to the profile page upon success

10. **index_view**: Displays all available URLs as clickable links.
    - Extracts and displays named URLs from the URL patterns

11. **virtual_basket_view**: Displays the user's virtual basket.
    - Retrieves and displays items in the user's basket
    - Calculates the total price and total items

12. **add_to_basket**: Adds an item to the user's basket.
    - Validates stock availability and updates the basket

13. **update_quantity**: Updates the quantity of an item in the user's basket.
    - Validates and updates the item quantity

14. **remove_from_basket**: Removes an item from the user's basket.
    - Removes the item and updates the stock quantity

15. **increment_quantity**: Increments the quantity of an item in the user's basket.
    - Validates and increments the item quantity

16. **decrement_quantity**: Decrements the quantity of an item in the user's basket.
    - Validates and decrements the item quantity

### URLs
The project includes several URL patterns to route requests to the appropriate views:

1. **printshop/urls.py**: Defines URL patterns for the printshop app.
    - Includes paths for product filtering, contact form, adding products, user registration, login, logout, profile, password change, basket management, and virtual basket

2. **fdmshop/urls.py**: Defines URL patterns for the entire project, including the admin interface and the printshop app.
    - Includes paths for the admin interface and the printshop app

### Admin
The project includes custom admin configurations to manage the models:

1. **CustomUserAdmin**: Custom admin interface for the CustomUser model.
    - Customizes the fieldsets, list display, list filter, and search fields
    - Adds actions to block and unblock users

2. **CategoryAdmin**: Admin interface for the Category model.
    - Customizes the list display, search fields, and ordering

3. **ProductAdmin**: Admin interface for the Product model.
    - Customizes the list display, search fields, list filter, and ordering
    - Defines fieldsets for the form view

4. **FilamentDetailsAdmin**: Admin interface for the FilamentDetails model.
    - Customizes the list display, search fields, and list filter

5. **CustomerAdmin**: Admin interface for the Customer model.
    - Customizes the list display, search fields, and ordering

6. **OrderAdmin**: Admin interface for the Order model.
    - Customizes the list display, search fields, list filter, and ordering

7. **OrderItemAdmin**: Admin interface for the OrderItem model.
    - Customizes the list display, search fields, list filter, and ordering

### Signals
The project includes a signal to prevent blocked users from logging in:

1. **prevent_blocked_login**: Signal handler to prevent blocked users from logging in.
    - Checks if the user is blocked and logs them out if they are
