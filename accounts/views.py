from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import admin_only, unauthenticated_user, allowed_users

# Create your views here.

@unauthenticated_user
def register_page(request):

    form = CreateUserForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            # getting user name to print in message
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name = 'customer')

            user.groups.add(group)
            messages.success(request, 'Account was created for: ' + username)

            return redirect('login')

    return render(request, 'accounts/register.html', context)

    """ Using login_required on every view we want to restrict, 
    like only after login user could see like products, customer etc.."""


@unauthenticated_user
def login_page(request):
 
    if request.method == "POST":
        # getting username and password to authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)

        # authenticate if there is a user
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context ={}
    return render(request, 'accounts/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


def user_page(request):
    context ={}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def customer(request, pk_test):

    customer = Customer.objects.get(id = pk_test)

    """ getting all orders, using customer child object"""    
    orders = customer.order_set.all()
    total_orders = orders.count()
    customer_name = customer.name
    customer_email = customer.email 
    customer_phone = customer.phone

    myFilter = OrderFilter(request.GET, queryset= orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'customer_email':customer_email,
        'customer_phone':customer_phone,
        'customer_name':customer_name,
        'myFilter':myFilter,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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
