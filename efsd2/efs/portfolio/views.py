from django.shortcuts import render,get_object_or_404
from .models import *
from .forms import *
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.http import HttpResponse
from django.views.generic import View
from portfolio.utils import render_to_pdf
from django.template.loader import get_template
from django.template.loader import render_to_string
from weasyprint import  HTML
import tempfile
from django.core.files.storage import FileSystemStorage
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.contrib.messages import constants as messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


now = timezone.now()
def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})

@login_required
def customer_new(request):
   if request.method == "POST":
       form = CustomerForm(request.POST)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.created_date = timezone.now()
           customer.save()
           customers = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customers})
   else:
       form = CustomerForm()
       # print("Else")
   return render(request, 'portfolio/customer_new.html', {'form': form})


@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})


@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')

@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})

@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   return redirect('portfolio:stock_list')

@login_required
def investment_list(request):
   investments = Investment.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})

@login_required
def investment_edit(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestmentForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           # stock.customer = stock.id
           investment.updated_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html', {'investments': investments})
   else:
       # print("else")
       form = InvestmentForm(instance=investment)
   return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   investment.delete()
   return redirect('portfolio:investment_list')

@login_required
def portfolio(request,pk):
   customer = get_object_or_404(Customer, pk=pk)
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
   #overall_investment_results = sum_recent_value-sum_acquired_value
   # Initialize the value of the stocks
   sum_current_stocks_value = 0
   sum_of_initial_stock_value = 0

   # Loop through each stock and add the value to the total
   for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()



   return render(request, 'portfolio/portfolio.html', {'customer': customer,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'sum_acquired_value': sum_acquired_value,
                                                       'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,})


def generate_pdf(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    # customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0

    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()
    html_string = render_to_string('portfolio/pdf_output.html', {'customer': customer,
                                                                            'investments': investments,
                                                                            'stocks': stocks,
                                                                            'sum_acquired_value': sum_acquired_value,
                                                                            'sum_recent_value': sum_recent_value,
                                                                            'sum_current_stocks_value': sum_current_stocks_value,
                                                                            'sum_of_initial_stock_value': sum_of_initial_stock_value, })
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=portfolio_summary.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    result = html.write_pdf(response, )
    return response

   #return response



# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('portfolio:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def mutualfund_list(request):
   funds = MutualFund.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/mutualfund_list.html', {'funds': funds})

@login_required
def mutualfund_new(request):
   if request.method == "POST":
       form = MutualFundForm(request.POST)
       if form.is_valid():
           fund = form.save(commit=False)
           fund.created_date = timezone.now()
           fund.save()
           funds = MutualFund.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/mutualfund_list.html',
                         {'funds': funds})
   else:
       form = MutualFundForm()
       # print("Else")
   return render(request, 'portfolio/mutualfund_new.html', {'form': form})

@login_required
def mutualfund_edit(request, pk):
   fund = get_object_or_404(MutualFund, pk=pk)
   if request.method == "POST":
       form = MutualFundForm(request.POST, instance=fund)
       if form.is_valid():
           fund = form.save()
           # stock.customer = stock.id
           fund.updated_date = timezone.now()
           fund.save()
           funds = MutualFund.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/mutualfund_list.html', {'funds': funds})
   else:
       # print("else")
       form = MutualFundForm(instance=fund)
   return render(request, 'portfolio/mutualfund_edit.html', {'form': form})

@login_required
def mutualfund_delete(request, pk):
   fund = get_object_or_404(MutualFund, pk=pk)
   fund.delete()
   return redirect('portfolio:mutualfund_list')
