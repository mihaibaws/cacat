from django import template
from cart.models import Order, OrderItem

register = template.Library()


@register.filter
def get_quantity(user):
    if user.is_authenticated:
        shit = OrderItem.objects.filter(is_ordered = False)
        return sum([item.quantity for item in shit.all()])

