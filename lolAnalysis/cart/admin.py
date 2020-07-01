from django.contrib import admin

# Register your models here.
from cart.models import OrderItem, Order, Payment
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)

