from rest_framework import serializers
from .models import OrderItem


class OrderItemSerializaer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('size',)
