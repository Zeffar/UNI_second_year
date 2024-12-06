from django import forms
from printshop.models import Category
from datetime import date
import re

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