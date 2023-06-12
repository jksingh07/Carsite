# Importing Libraries

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Creating a class for car type model
class CarType(models.Model):
    name = models.CharField(max_length=150)

# Vehicle Model
class Vehicle(models.Model):
    car_type = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
    car_name = models.CharField(max_length=200)
    car_price = models.DecimalField(max_digits=10, decimal_places=6)
    inventory = models.PositiveIntegerField(default=10)
    instock = models.BooleanField(default=True)

class Buyer(User):
    AREA_CHOICES = [
    ('W', 'Windsor'),
    ('LS', 'LaSalle'),
    ('A', 'Amherstburg'),
    ('L', 'Lakeshore'),
    ('LE', 'Leamington'),]

    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    area=models.CharField(max_length=2, choices=AREA_CHOICES, default='A')
    interested_in = models.ManyToManyField(CarType)

class OrderVehicle(models.Model):
    # We do have 4 different choices for the orders.
    ORDER_STATUS_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Placed'),
        (2, 'Shipped'),
        (3, 'Delivered'),
    ]


    #! OrderVehicle has relation with the vehicle using Vehicle foreign key
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    #! OrderVehicle has also another relation with Buyer table using buyer as foreign key
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    # A field named quantity in order to get the quantity of the vehicles
    quantity = models.PositiveIntegerField()
    # Field for checking and showing the status of the order.
    # The choices of the order is limited by the ORDER_STATUS_CHOICES which has been coded above.
    # 4.	A field indicating the status of an order. These statuses can be with choices {0,1,2,3} such as:
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    # 5.	A date field indicating the date when an order was last updated
    last_updated = models.DateField(auto_now=True)


    # Dunder method to show a formatted text in the admin page with the following format
    # ID by BuyerUsername for Vehicle car name
    def __str__(self):
        return f'Order {self.id} by {self.buyer.username} for {self.vehicle.car_name}'

    # VII.	For the OrderVehicle model, write a method def total_price(self). This method should return the total price for all the Vehicles in the order.
    def total_price(self):
        return self.quantity * self.vehicle.car_price

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Our new Model named Description -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
class Description(models.Model):
    # A field with the format of character with the maximum length of 200 characters
    title = models.CharField(max_length=200)
    # A field with the format of text field with no parameters
    description = models.TextField()
    # A field with the format of DateTime with the option of auto new add.
    date_added = models.DateTimeField(auto_now_add=True)


    # A dunder method in which the title of the description will be shown in the admin page
    def __str__(self):
        return self.title