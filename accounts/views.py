from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import *
# Create your views here.

def home(request):

    """Rendering html pages"""
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status = 'Delivered').count()
    orders_pending = orders.filter(status = 'Pending').count()

    context = {
        'orders':orders, 
        'customers':customers, 
        'total_orders':total_orders, 
        'orders_delivered':orders_delivered,
        'orders_pending':orders_pending
        }
    
    return render(request, 'accounts/dashboard.html', context)


def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk_test):
    customer = Customer.objects.get(id = pk_test)
    
    # getting all orders, using customer child object
    orders = customer.order_set.all()
    total_orders = orders.count()
    customer_name = customer.name
    customer_email = customer.email
    customer_phone = customer.phone


    
    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'customer_email':customer_email,
        'customer_phone':customer_phone,
        'customer_name':customer_name

    }
    return render(request, 'accounts/customer.html', context)


def create_order(request, pk):
 
# inline forms(inlineformset_factory) are creating multiple forms with in one forms, takes in parent and child model.
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ['product', 'status'], extra = 8)

    customer = Customer.objects.get(id = pk)
    # adding queryset to unable preselected optiono in creating orders form
    formset = OrderFormSet(queryset = Order.objects.none(), instance = customer)
    # Retrieving forms data, # from forms.py file
    # form = OrderForm(initial = { 'customer' : customer } ) 

    if request.method == 'POST':
        # print('Printin POST information: ', request.POST)
        # Created order with token generated csrfmiddlewaretoken
        # saving data into form after authentication, then redirect back to main dashboard

        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)

        # if form.is_valid:
        #     form.save()
        #     return redirect('/')
        if formset.is_valid:
            formset.save()
            return redirect('/')

    context = {
        'formset':formset,
        'customer': customer
    }
    return render(request, 'accounts/create_order.html', context)


# creating update order method
def update_order(request, pk):

    order = Order.objects.get( id = pk) #using pk to prefetch prev data for updation
    form = OrderForm(instance = order) # creating instance to prefill form for update query

    context = {
        'form':form
    }

    if request.method == 'POST':
    # print('Printin POST information: ', request.POST)
    # Created order with token generated csrfmiddlewaretoken
    # saving data into form after authentication, then redirect back to main dashboard

        form = OrderForm(request.POST, instance=order) # instance to Post updated form rather than new
        if form.is_valid:
            form.save()
            return redirect('/')

    return render(request, 'accounts/create_order.html', context)


def delete_order(request, pk):
    # form = OrderForm(instance = order) # creating instance to delete item
    order = Order.objects.get( id = pk) #using pk to delete specific item

    context = {
        'order':order
    }
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete.html', context)
