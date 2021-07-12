from rest_framework import serializers
from .models import Customer,Stock,Investment
from djmoney.contrib.django_rest_framework import MoneyField


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
            model = Customer
            fields = ('name', 'address', 'cust_number', 'city', 'state', 'zipcode', 'email', 'email', 'cell_phone')

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'amount', 'amount_currency')

class Serializers(serializers.Serializer):
    amount = MoneyField(max_digits=10, decimal_places=2)