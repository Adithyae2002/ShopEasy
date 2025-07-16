"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import vendor_profile, edit_vendor_profile
from . import views

   


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/',views.home),
    path('register/', views.register_view, name='register'),
    path('userregister/', views.user_register, name='userregister'),
    path('login/', views.login_view, name='login'),
    path('loginforms/', views.user_login, name='loginforms'),
    path('logout/',views.logout_view, name='logout'),  # Correct URL pattern
    path('products/',views.product_list,name='products'),
    # path('products.html', views.product_list), 
    path('product_detail/<int:product_id>/',views.product_detail,name='product_detail'),


#cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),  # Update cart for a specific product
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove product from cart
    path('checkout/',views.checkout, name='checkout'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),  # Buy now view
    path('account_management/',views.account_managements, name='account_managements'),  # URL for account management
    path('account_management/orders/', views.view_order_history, name='account_orders'),
    path('edit_account/',views.edit_account, name='edit_account'),  # URL for editing account information
    path('add_payment_method/',views.add_payment_method, name='add_payment_method'),  # URL for adding payment method
    path('view_cart/',views.view_cart, name='view_cart'), 
    path('process_order/',views.process_order, name='process_order'),
    path('order_confirmation/<int:order_id>/',views.order_confirmation, name='order_confirmation'),



 # wishlist

    path('wishlist/',views.wishlist_view, name='wishlist_view'),  # Define the URL pattern and name it 'wishlist'  
    path('add_to_wishlist/<int:item_id>/',views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/',views.remove_from_wishlist, name='remove_from_wishlist'),
    path('items/',views.item_list, name='item_list'),  # URL pattern for item list

# admin
    path('landing/', views.admin_home, name='admin_home'),  # Admin home page
    path('manage_products/', views.manage_products, name='manage_products'),  # Manage products page
    path('manage_orders/',  views.OrderListView.as_view(), name='manage_orders'),
    path('manage_orders/<str:order_id>/', views.OrderDetailView.as_view(), name='order_details'),
    path('account/',views.account_management, name='account_management'),
    path('add-product/', views.add_product, name='add_product'),  # Add new product page
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),  # Edit product page
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),  # Delete product page
    path('admin_profile/',views.admin_profile, name='admin_profile'),
    
   
#vendor
    path('dashboard/',views.vendor_dashboard, name='vendor_dashboard'),
    path('add/',views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',views.delete_product, name='delete_product'),
    path('order-tracking/', views.order_tracking, name='order_tracking'),
    path('update-order-status/<int:order_id>/',views.update_order_status, name='update_order_status'),
    path('vendor/profile/',views.vendor_profile, name='vendor_profile'),
    path('vendor/profile/edit/',views.edit_vendor_profile, name='edit_vendor_profile'),
    path('vendor/logout/',views.vendor_logout, name='vendor_logout'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



