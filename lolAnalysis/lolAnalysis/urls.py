
"""lolAnalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from main.views import main_view, player_info, game_wiki
from users.views import register
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Profile.views import Profile_view
from products.views import (
    ProductListView,
    ProductDetailView,
    ProductDeleteView,
    product_form_view,
    )
from cart.views import(
    add_to_cart,
    delete_from_cart,
    remove_single_item_from_cart,
    order_details,
    CheckoutView,
    PaymentView,
    success_payment
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name = 'home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),

    path('lol-wiki/', game_wiki, name = 'lol-wiki'),
    path('player-info/<region>/<summoner_name>/',player_info, name='player-info'),
    path('profile/',Profile_view, name = 'profile'),
    path('products/',ProductListView.as_view(), name = 'products'),
    path('products/<slug>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('addproduct/', product_form_view, name = 'product-create'),
    path('products/<slug>/delete/', ProductDeleteView.as_view(), name = 'product-delete'),

    
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('order-summary/', order_details, name='order-summary'),
    path('item/delete/<slug>/', delete_from_cart, name='delete-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('checkout/', CheckoutView, name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('success-payment', success_payment, name = 'success-payment')


] 


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
