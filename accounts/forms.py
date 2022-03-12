from calendar import c
from django.forms import ModelForm
from .models import *

# creaing class for creating orders
class OrderForm(ModelForm):
    
    # creating meta class to allow user to add data using Order model fields
    class Meta:
        model = Order   # list Order model fields
        fields = "__all__"  # allow all Order fields to create order
        # fields = ['customer', 'status']  # incase only allow customer and status fields from Order fields
