from django import forms
from printshop.models import Category
from datetime import date
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, FilamentDetails, CustomUser
from decimal import Decimal

class FilamentFilterForm(forms.Form):
    material = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Material'}))
    color = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Color'}))
    min_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Min Price'}))
    max_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max Price'}))
    stock_min = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Min Stock'}))
    stock_max = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max Stock'}))
    brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Brand'}))
    diameter = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Diameter'}))
    weight = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Weight'}))

def validate_name(value):
    """Validate that the value starts with an uppercase letter and contains only letters and spaces."""
    if not value[0].isupper():
        raise forms.ValidationError("The value must start with an uppercase letter.")
    if not all(char.isalpha() or char.isspace() for char in value):
        raise forms.ValidationError("The value must contain only letters and spaces.")

def validate_message(value):
    """Validate that the message contains 5-100 words, no links, and ends with the user's name."""
    words = re.findall(r'\b\w+\b', value)
    if len(words) < 5 or len(words) > 100:
        raise forms.ValidationError("The message must contain between 5 and 100 words.")
    if any(word.startswith(("http://", "https://")) for word in words):
        raise forms.ValidationError("The message must not contain links.")
    # The name check will be added dynamically in the view based on the user input.

class ContactForm(forms.Form):

    nume = forms.CharField(
        max_length=10,
        required=True,
        validators=[validate_name],
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
    )
    prenume = forms.CharField(
        required=False,
        validators=[validate_name],
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
    )
    data_nasterii = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    confirmare_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Confirm Email'}))
    tip_mesaj = forms.ChoiceField(
        choices=[
            ('reclamatie', 'Reclamatie'),
            ('intrebare', 'Intrebare'),
            ('review', 'Review'),
            ('cerere', 'Cerere'),
            ('programare', 'Programare'),
        ],
        required=True
    )
    subiect = forms.CharField(
        required=True,
        validators=[validate_name],
        widget=forms.TextInput(attrs={'placeholder': 'Subject'}),
    )
    minim_zile_asteptare = forms.IntegerField(
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Minimum Waiting Days'}),
    )
    mesaj = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Please sign your name at the end'}),
        label="Message (please sign your name at the end)"
    )

    def clean(self):
        """Custom validation logic."""
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirmare_email')
        data_nasterii = cleaned_data.get('data_nasterii')
        mesaj = cleaned_data.get('mesaj')
        nume = cleaned_data.get('nume')

        # Validate email confirmation
        if email != confirm_email:
            raise forms.ValidationError("Email and confirmation email must match.")

        # Validate user age
        if data_nasterii:
            today = date.today()
            age_years = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
            if age_years < 18:
                raise forms.ValidationError("The sender must be an adult (18+ years).")

        # Validate message ends with the user's name
        if mesaj and nume and not mesaj.strip().endswith(nume):
            raise forms.ValidationError("The message must end with your name as a signature.")

        return cleaned_data
    

class ProductForm(forms.ModelForm):
    # Fields specific to filaments
    material = forms.ChoiceField(
        choices=[
            ('PLA', 'PLA'),
            ('PETG', 'PETG'),
            ('ABS', 'ABS'),
            ('TPU', 'TPU'),
        ],
        required=True,
        label="Material",
        error_messages={'required': 'Please select a material.'}
    )
    color = forms.CharField(
        required=True,
        label="Color",
        error_messages={'required': 'Please enter a color.'}
    )
    diameter = forms.DecimalField(
        required=True,
        min_value=0.1,
        max_value=5.0,
        label="Diameter (mm)",
        help_text="Enter the diameter of the filament in millimeters.",
        error_messages={'required': 'Please provide a diameter.', 'invalid': 'Enter a valid number.'}
    )
    weight = forms.DecimalField(
        required=True,
        min_value=1,
        max_value=5000,
        label="Weight (grams)",
        help_text="Enter the weight of the filament in grams.",
        error_messages={'required': 'Please provide a weight.', 'invalid': 'Enter a valid number.'}
    )

    # Additional fields
    quantity_to_add = forms.IntegerField(
        min_value=1,
        label="Quantity to Add",
        help_text="Enter the number of items to add to stock.",
        error_messages={'required': 'Please provide a quantity to add.'}
    )
    user_initials = forms.CharField(
        max_length=5,
        label="User Initials",
        error_messages={'required': 'Please enter your initials.'}
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity_to_add', 'user_initials', 'material', 'color', 'diameter', 'weight']
        labels = {
            'name': 'Product Name',
            'price': 'Price per Unit',
        }
        error_messages = {
            'name': {'required': 'Product name is required.'},
            'price': {'required': 'Price is required.', 'invalid': 'Enter a valid price.'},
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < Decimal('0.01'):
            raise forms.ValidationError("Price must be at least $0.01.")
        return price

    def clean_quantity_to_add(self):
        quantity = self.cleaned_data.get('quantity_to_add')
        if quantity and quantity > 1000:
            raise forms.ValidationError("You cannot add more than 1000 units at once.")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        quantity_to_add = cleaned_data.get('quantity_to_add')

        if price and quantity_to_add:
            total_value = price * Decimal(quantity_to_add)
            if total_value > Decimal('1000000.00'):
                raise forms.ValidationError("Total value of stock cannot exceed $1,000,000.")

        return cleaned_data

    def save(self, commit=True):
        # Save the product first with commit=False
        product = super().save(commit=False)

        # Automatically set the category to "Filaments"
        try:
            filaments_category = Category.objects.get(name="Filaments")
        except Category.DoesNotExist:
            raise forms.ValidationError("The 'Filaments' category does not exist. Please create it in the admin panel.")
        product.category = filaments_category

        # Calculate excluded fields
        product.total_value = self.cleaned_data['price'] * Decimal(self.cleaned_data['quantity_to_add'])
        product.added_by = self.cleaned_data['user_initials']

        if commit:
            product.save()

        # Save filament-specific details
        filament_details = FilamentDetails(
            product=product,
            material=self.cleaned_data['material'],
            color=self.cleaned_data['color'],
            diameter=self.cleaned_data['diameter'],
            weight=self.cleaned_data['weight']
        )
        if commit:
            filament_details.save()

        return product
    

class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(required=True, max_length=15, label="Phone Number")
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    address = forms.CharField(required=True, widget=forms.Textarea, label="Address")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")
    bio = forms.CharField(required=True, widget=forms.Textarea, label="Bio")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'date_of_birth', 'address', 'profile_picture', 'bio', 'password1', 'password2']

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        from datetime import date
        if (date.today().year - dob.year) < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return dob

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError("Phone number must be between 10 and 15 digits.")
        return phone

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if len(bio.split()) < 10:
            raise forms.ValidationError("Bio must contain at least 10 words.")
        return bio
    
class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Remember Me")

