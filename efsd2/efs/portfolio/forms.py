from django import forms
from .models import Customer, Stock, Investment,MutualFund
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cust_number', 'name', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone',)

class StockForm(forms.ModelForm):
   class Meta:
       model = Stock
       fields = ('customer', 'symbol', 'name', 'shares', 'purchase_price', 'purchase_date',)

class InvestmentForm(forms.ModelForm):
   class Meta:
       model = Investment
       fields = ('customer', 'category', 'description', 'acquired_value', 'acquired_date', 'recent_value','recent_date',)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    # phone_number = forms.CharField(max_length=10)
    zip_code = forms.CharField(max_length=10)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'zip_code',
                  'email', 'password1', 'password2',)

class MutualFundForm(forms.ModelForm):
   class Meta:
       model = MutualFund
       fields = ('customer', 'scheme', 'investment_amount', 'acquired_value', 'acquired_date', 'recent_value','recent_date',)