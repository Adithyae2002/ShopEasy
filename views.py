from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from .models import *
from django.contrib.auth import logout


# Home Page view
def home(request):
    return render(request,'home.html')


# Product listing view
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

# Product detail view
def product_detail(request, product_id):
    product = Product.objects.get (id=product_id)
    return render(request, 'product_detail.html', {'product': product})



# Register View
def register(request):
    return render(request, 'register.html')

def user_register(request):
    if request.method == "POST":
        # Safely retrieve form data using get()
        username = request.POST.get('uname')
        useremail = request.POST.get('email')
        password = request.POST.get('pass')
        password2 = request.POST.get('pass2')

        # Check if all fields are provided
        if not username or not useremail or not password or not password2:
            return render(request, 'register.html', {'error': 'Please fill in all fields.'})

        # Password validation
        if password != password2:
            return render(request, 'register.html', {'error': "Passwords do not match"})

        # Save user
        try:
            # Check if the email already exists
            Userreg.objects.get(Useremail=useremail)
            return render(request, 'register.html', {'error': 'Email already exists'})
        except Userreg.DoesNotExist:
            reg = Userreg(Username=username, Useremail=useremail, Password=make_password(password))
            reg.save()
            return redirect('login/')  # Redirect to login page

    return render(request, 'register.html')
        
# Login View
def user_login(request):
    if request.method == 'POST':
        # Safely retrieve form data using get()
        email = request.POST.get('email')
        password = request.POST.get('pass')

        # Check if both fields are provided
        if not email or not password:
            return render(request, 'login.html', {'error': 'Please fill in all fields.'})

        # Admin login
        if email == 'admin@gmail.com' and password == 'admin123':
            request.session['logindetail'] = email
            request.session['admin'] = 'admin'
            return redirect('home/')  # Redirect to admin home

        # User login
        try:
            user = Userreg.objects.get(Useremail=email)  # Fetch user by email
            if check_password(password, user.Password):  # Verify password
                # Set session variables for the logged-in user
                request.session['uid'] = user.id
                request.session['email'] = user.Useremail
                return redirect('home')  # Redirect to user home
            else:
                return render(request, 'login.html', {'error': 'Invalid password'})
        except Userreg.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email'})
    
    # Render the login page for GET requests
    return render(request, 'login.html')

from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect

def logout_view(request):
    if request.method == 'POST':
        django_logout(request)  # Use the imported Django logout function
        return redirect('home')  # Redirect to home or login page
    return render(request, 'logout.html')  # Render the logout confirmation page
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use get() to safely retrieve form data
        password = request.POST.get('password')  # Use get() for password as well
        
        if username and password:  # Check if both fields are provided
            user = authenticate(request, username=username, password=password)  # Authenticate the user
            
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('home')  # Redirect to home after login
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})  # Show error message
        else:
            return render(request, 'login.html', {'error': 'Please fill in all fields.'})  # Handle empty fields
    
    return render(request, 'login.html')  # Render the login page for GET requests

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use get() to safely retrieve form data
        password = request.POST.get('password')  # Use get() for password as well
        
        if username and password:  # Check if both fields are provided
            User.objects.create_user(username=username, password=password)  # Create a new user
            return redirect('login')  # Redirect to login page after registration
        else:
            return render(request, 'register.html', {'error': 'Please fill in all fields.'})  # Handle empty fields
    
    return render(request, 'register.html')  # Render the registration page
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User  # Import your User model

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use get() to safely retrieve form data
        password = request.POST.get('password')  # Use get() for password as well
        
        if username and password:  # Check if both fields are provided
            user = authenticate(request, username=username, password=password)  # Authenticate the user
            
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('home')  # Redirect to home after login
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        else:
            return render(request, 'login.html', {'error': 'Please fill in all fields.'})  # Handle empty fields
    
    return render(request, 'login.html')  # Render the login page for GET requests
# shop/views.py


from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product

def cart(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
    else:
        return redirect('login')

    return render(request, 'cart.html', {'cart': cart})

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_price = cart.get_total_price()  # Get the total price
        return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})
    else:
        return redirect('login')  
    
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        cart.save()
        return redirect('cart')
    else:
        return redirect('login')\
        
def update_cart(request, product_id):
    cart = Cart(request)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart.update(product_id, quantity)  # Assuming you have an update method in your Cart class
    return redirect('cart')  # Redirect to the cart page after updating


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart.products.remove(product)
        cart.save()
        return redirect('cart')
    else:
        return redirect('login')
    
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product or return 404
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)  # Get the quantity from the form
        cart = Cart(request)
        cart.add(product, quantity)  # Add the product to the cart with the specified quantity
        return redirect('cart')  # Redirect to the cart page after adding

    return render(request, 'buy_now.html', {'product': product})  # Render the buy now page

# views.py
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from .models import Order  # Assuming you have an Order model

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the order
            order = Order.objects.create(
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                payment_method=form.cleaned_data['payment_method'],
                # Add other fields as necessary
            )
            # Redirect to the order confirmation page
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    
    return render(request, 'checkout.html', {'form': form})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Use get_object_or_404 for better error handling
    return render(request, 'order_confirmation.html', {'order': order})
    # Checkout view
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Order, OrderItem

#  # Assuming you have an Order model

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                payment_method=form.cleaned_data['payment_method'],
            )
            return redirect('order-confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    
    return render(request, 'checkout.html', {'form': form})
# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Order, Cart  # Assuming you have an Order model and Cart model

def process_order(request):
    if request.method == 'POST':
        # Extract data from the form
        customer_name = request.POST.get('customer_name')
        shipping_address = request.POST.get('shipping_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        contact_number = request.POST.get('contact_number')

        # Assuming you have a Cart model that holds the user's cart items
        cart = Cart.objects.get(user=request.user)  # Get the user's cart
        total_amount = cart.get_total_price()  # Calculate the total amount

        # Create an order instance
        order = Order.objects.create(
            customer_name=customer_name,
            shipping_address=shipping_address,
            city=city,
            state=state,
            zip_code=zip_code,
            contact_number=contact_number,
            total_amount=total_amount,  # Include the total amount
            # Add any other necessary fields
        )

        # Optionally, add a success message
        messages.success(request, 'Your order has been placed successfully!')

        # Redirect to the order confirmation page
        return redirect(reverse('order_confirmation', args=[order.id]))

    # If the request method is not POST, render the checkout page
    return render(request, 'checkout.html')

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist, Item
from .models import Item
from .forms import ItemForm

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.all()
    return render(request, 'wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Assuming you have a Wishlist model that links users to products
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.items.add(product)  # Assuming 'items' is a ManyToManyField in your Wishlist model

    return redirect('wishlist')  # Redirect to the wishlist page or wherever you want

@login_required
def remove_from_wishlist(request, item_id):
    # Assuming 'item_id' refers to a Product ID in the wishlist
    product = get_object_or_404(Product, id=item_id)  # Change this if 'item_id' refers to something else
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.items.remove(product)  # Ensure this is removing the correct product
    return redirect('wishlist')  # Redirect to the wishlist page or wherever you want
def item_list(request):

    items = Item.objects.all()  # Fetch all items
    return render(request, 'item_list.html', {'items': items})  # Render the item list template


# Order confirmation view
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Retrieve the order by ID
    return render(request, 'order_confirmation.html', {'order': order})

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order  # Assuming you have an Order model
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from .models import PaymentMethod
from .models import Profile
from .forms import ProfileUpdateForm
@login_required  # Ensure the user is logged in
def account_managements(request):
    user = request.user
    orders = Order.objects.filter(customer_name=user.username)  # Adjust this based on your model
    return render(request, 'account_management.html', {'user': user, 'orders': orders})
@login_required
def edit_account(request):
    # Get the user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Create a form instance with the submitted data and the current profile instance
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('account_managements')  # Redirect to account management page
    else:
        # Pre-fill the form with the current profile data
        form = ProfileUpdateForm(instance=profile)

    # Render the edit account template with the form
    return render(request, 'edit_account.html', {'form': form})
def add_payment_method(request):
    if request.method == 'POST':
        # Extract payment method details from the form
        payment_type = request.POST.get('payment_type')  # e.g., 'Card', 'UPI'
        details = request.POST.get('details')  # e.g., card number, UPI ID

        # Create a new payment method instance
        PaymentMethod.objects.create(
            user=request.user,  # Assuming you have a user field in your PaymentMethod model
            type=payment_type,
            details=details
        )

        messages.success(request, 'Payment method added successfully!')
        return redirect('account_managements')  # Redirect to account management page

    return render(request, 'add_payment_method.html')  # Render the form for adding payment method


@login_required
def view_cart(request):
    # Here you would typically retrieve the user's cart items from the session or a cart model
    # For simplicity, we'll assume you have a Cart model that links to the user
    cart_items = []  # Replace this with actual logic to retrieve cart items
    total_price = 0  # Initialize total price

    # Example logic to calculate total price (if you have a Cart model)
    # cart = Cart.objects.get(user=request.user)
    # cart_items = cart.items.all()  # Assuming you have a related name for cart items
    # total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def view_order_history(request):
    user = request.user
    # Use customer_name instead of customer
    orders = Order.objects.filter(customer_name=user.username)  # Retrieve orders for the logged-in user
    return render(request, 'order_history.html', {'orders': orders})
# logout
def logout(request):
    logout(request)
    return redirect('login')

# Account page view 
def account(request):
    return render(request,'account.html')

#Admin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order  # Assuming you have Product and Order models
from .forms import ProductForm  # Assuming you have a ProductForm for adding/editing products
from django.views import View
from .models import Order, OrderItem

# View for the admin landing page
def admin_home(request):
    return render(request, 'landing.html')

# View for managing products
def manage_products(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'manage_products.html', {'products': products})

# View for managing orders

class OrderListView(View):
    def get(self, request):
        orders = Order.objects.all().order_by('-order_date')
        return render(request, 'order_list.html', {'orders': orders})

class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        return render(request, 'order_details.html', {'order': order})

    def post(self, request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
        return render(request, 'order_details.html', {'order': order})

# views.py
from django.shortcuts import render

def account_management(request):
    # Logic for account management can go here
    return render(request, 'account.html')  # Ensure you have this template
# View for adding a new product
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
# View for editing a product
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

# View for deleting a product
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('manage_products')
    return render(request, 'delete_product.html', {'product': product})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderStatusUpdateForm

# View for managing orders
def manage_orders(request):
    orders = Order.objects.all()  # Fetch all orders
    return render(request, 'manage_orders.html', {'orders': orders})

# View for order details
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Fetch the specific order
    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)  # Bind the form with the order instance
        if form.is_valid():
            form.save()  # Update order status
            return redirect('manage_orders')  # Redirect to order management page
    else:
        form = OrderStatusUpdateForm(instance=order)  # Pre-fill the form with the current order data
    return render(request, 'order_details.html', {'order': order, 'form': form})

# View for processing returns (optional)
def process_return(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Implement return processing logic here
    # For example, you might want to update the order status or notify the customer
    return redirect('manage_orders')  # Redirect back to the order management page

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AdminProfile
from .forms import AdminProfileForm

@login_required
def admin_profile(request):
    profile = get_object_or_404(AdminProfile, user=request.user)  # Get the admin's profile
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('profile')  # Redirect to the profile page
    else:
        form = AdminProfileForm(instance=profile)  # Pre-fill the form with current profile data
    return render(request, 'admin_profile.html', {'form': form, 'profile': profile})


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AdminProfile
from .forms import AdminAccountForm, AdminProfileForm

@login_required
def account_management(request):
    profile = get_object_or_404(AdminProfile, user=request.user)  # Get the admin's profile
    if request.method == 'POST':
        account_form = AdminAccountForm(request.POST, instance=request.user)
        profile_form = AdminProfileForm(request.POST, instance=profile)
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()  # Save the updated account information
            profile_form.save()  # Save the updated profile information
            return redirect('account_management')  # Redirect to the account management page
    else:
        account_form = AdminAccountForm(instance=request.user)  # Pre-fill the form with current user data
        profile_form = AdminProfileForm(instance=profile)  # Pre-fill the form with current profile data
    return render(request, 'account.html', {
        'account_form': account_form,
        'profile_form': profile_form,
        'profile': profile
    })
# views.py
# from django.contrib.auth import logout
# from django.shortcuts import redirect

# def logouts(request):
#     logout(request)  # Log the user out
#     return redirect('admin_home')  # Redirect to the login page

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

def vendor_dashboard(request):
    # Fetch all products for the vendor
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm()
    return render(request, 'vadd_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'vedit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('vendor_dashboard')
    return render(request, 'vconfirm_delete.html', {'product': product})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def order_tracking(request):
    # Fetch orders associated with the logged-in vendor
    orders = Order.objects.filter(vendor=request.user)
    return render(request, 'order_tracking.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, vendor=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            return redirect('order_tracking')
    return render(request, 'update_order_status.html', {'order': order})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VendorProfile
from .forms import VendorProfileForm

@login_required
def vendor_profile(request):
    # Get the vendor's profile
    profile = get_object_or_404(VendorProfile, user=request.user)
    return render(request, 'vendor_profile.html', {'profile': profile})
    from .forms import VendorProfileForm

@login_required
def edit_vendor_profile(request):
    # Get the vendor's profile
    profile = get_object_or_404(VendorProfile, user=request.user)

    if request.method == 'POST':
        # Bind the form with the submitted data and the current profile instance
        form = VendorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('vendor_profile')  # Redirect to the profile page
    else:
        # Pre-fill the form with the current profile data
        form = VendorProfileForm(instance=profile)

    return render(request, 'edit_vendor_profile.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def vendor_logout(request):
    logout(request)  # End the vendor's session
    return redirect('login')  # Redirect to the login page