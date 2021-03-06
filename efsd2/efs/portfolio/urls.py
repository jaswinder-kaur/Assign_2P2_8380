from django.conf.urls import url
from . import views
from django.urls import path,re_path
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views

app_name = 'portfolio'
urlpatterns = [

    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^home/$', views.home, name='home'),
    path('signup', views.signup, name="signup"),
    path('customer/create/', views.customer_new, name='customer_new'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_new, name='stock_new'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('stock/<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    path('investment_list', views.investment_list, name='investment_list'),
    path('investment/create/', views.investment_new, name='investment_new'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investment/<int:pk>/delete/', views.investment_delete, name='investment_delete'),
    path('customer/<int:pk>/portfolio/', views.portfolio, name='portfolio'),
    url(r'^customers_json/', views.CustomerList.as_view()),
    url(r'^generate/pdf/(?P<pk>\d+)$', views.generate_pdf, name='generate_pdf'),
    path('mutualfund_list', views.mutualfund_list, name='mutualfund_list'),
    path('mutualfund/create/', views.mutualfund_new, name='mutualfund_new'),
    path('mutualfund/<int:pk>/edit/', views.mutualfund_edit, name='mutualfund_edit'),
    path('mutualfund/<int:pk>/delete/', views.mutualfund_delete, name='mutualfund_delete'),


    #  path('export_pdf', views.export_pdf, name='export_pdf'),


]

urlpatterns = format_suffix_patterns(urlpatterns)

