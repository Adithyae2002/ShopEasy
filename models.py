from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    useremail = models.EmailField(unique=True)  # Ensure this field exists


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
   
from django.db import models

class Userreg(models.Model):
    username = models.CharField(max_length=150)  # Correct field name
    useremail = models.EmailField()               # Correct field name
    password = models.CharField(max_length=128)   # Correct field name  # Use hashed passwords
    password2 = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, default='Not Provided')
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    ], default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)  # Add this field
    state = models.CharField(max_length=100)  # Add this field
    zip_code = models.CharField(max_length=20)  # Add this field
    shipping_address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"   
    def __str__(self):
        return f"Order of {self.customer_name} on {self.order_date}"
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Assuming you have a Product model
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']  

    def __str__(self):
        return f"Order Item {self.id} - {self.product.name} (Quantity: {self.quantity})"
    def __str__(self):
        return f"{self.product.name} (Qty: {self.quantity})"

class loginform(models.Model):
    Username = models.CharField(max_length=200)
    password= models.CharField(max_length=200)

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def get_total_price(self):
        total = sum(product.price for product in self.products.all())
        return total

# models.py
from django.db import models
from django.contrib.auth.models import User

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    type = models.CharField(max_length=50)  # e.g., 'Card', 'UPI'
    details = models.CharField(max_length=255)  # e.g., card number, UPI ID

    def __str__(self):
        return f"{self.type} - {self.details}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pics/', default='default_profile.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


    def __str__(self):
        return self.user.username

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as necessary

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')

    def _str_(self):
        return f"{self.user.username}'s Wishlist"
        
class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

