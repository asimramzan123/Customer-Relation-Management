from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Using dynamic name links for urls instead passing complete page link
    path('login/', views.login_page, name = 'login'),
    path('logout/', views.logout_page, name = 'logout'),
    path('register/', views.register_page, name = 'register'),
    
    path('', views.home, name = 'home'),
    path('products/', views.product, name = 'product'),
    path('customer/<str:pk_test>/', views.customer, name= 'customer' ),

    path('create_order/<str:pk>/', views.create_order, name = 'create_order'),
    path('update_order/<str:pk>/', views.update_order, name = 'update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name = 'delete_order'),

]
