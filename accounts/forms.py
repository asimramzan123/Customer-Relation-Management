from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']


# creaing class for creating orders
class OrderForm(ModelForm):
    
    # creating meta class to allow user to add data using Order model fields
    class Meta:
        model = Order   # list Order model fields
        fields = "__all__"  # allow all Order fields to create order
        # fields = ['customer', 'status']  # incase only allow customer and status fields from Order fields


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User   # list Order model fields
        fields = ['username', 'email', 'password1', 'password2'] 