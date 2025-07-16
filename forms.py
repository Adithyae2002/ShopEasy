from django import forms
from .models import VendorProfile
from .models import Order
from .models import Product
from .models import Item
from .models import AdminProfile
from .models import Profile
from django.contrib.auth.models import User

class CheckoutForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    # Add other fields as necessary
    class Meta:
        model = Order
        fields = ['customer_name', 'address']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']

class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  

        # forms.py

class AdminAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Fields to update

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['contact_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price']


class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ['contact_number', 'address', 'profile_picture']
