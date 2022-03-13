from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length= 150, null = True)
    phone = models.CharField(max_length= 150, null = True)
    email = models.CharField(max_length= 150, null = True)
    date_created = models.DateTimeField(auto_now_add=True, null = True)

# printing customer name in added field
    def __str__(self) :
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length= 150, null = True)


    def __str__(self) :
        return self.name


class Product(models.Model):

    Product_Category = [
        ('In_Door', 'In_Door'),
        ('Out_Door', 'Out_Door')
    ]
    name = models.CharField(max_length=10,  null = True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=150, null=True, choices= Product_Category)
    description = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)


    def __str__(self) :
        return self.name


class Order(models.Model):

    ORDER_PENDING = 'Pending'
    ORDER_OUT = 'Not in Stock'
    ORDER_DELIVERED = 'Delivered'

    STATUS = [
    
        (ORDER_PENDING, 'Pending'), 
        (ORDER_OUT, 'Out of Stock'),
        (ORDER_DELIVERED, 'Delivered'),
    ]
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL )
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50,  null = True, choices= STATUS, default=ORDER_PENDING)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    note = models.CharField(max_length=50,  null = True,)

    def __str__(self) :
        return self.product.name
    
