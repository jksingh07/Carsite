# Django's import statement for including the models module
from django.db import models

# Django's import statement for including the User model from the auth app
from django.contrib.auth.models import User


# Definition of CarType model
class CarType(models.Model):
    # The field name of type CharField with a maximum length of 150
    name = models.CharField(max_length=150)

    # Dunder method which is responsible for showing the name of the car, which is coded as a field of the CarType
    # in the admin page.
    def __str__(self):
        return self.name

# Definition of Vehicle model
class Vehicle(models.Model):
    # The field car_type of type ForeignKey which references CarType model
    # The related_name argument is used for reverse relation from CarType to Vehicle
    # on_delete argument specifies what happens when referenced object is deleted
    car_type = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
    # The field car_name of type CharField with a maximum length of 200
    car_name = models.CharField(max_length=200)
    # The field car_price of type DecimalField with a maximum of 10 digits and 6 decimal places
    car_price = models.DecimalField(max_digits=10, decimal_places=2)
    # The field inventory of type PositiveIntegerField with a default value of 10
    inventory = models.PositiveIntegerField(default=10)
    # The field instock of type BooleanField with a default value of True
    instock = models.BooleanField(default=True)
   # II.	Add an optional field in the Vehicle table which describes the product in a few words. This should be a text field
    description = models.TextField(blank=True)

    # New field for car features
    CRUISE_CONTROL = 'CC'
    AUDIO_INTERFACE = 'AI'
    AIRBAGS = 'AB'
    AIR_CONDITIONING = 'AC'
    SEAT_HEATING = 'SH'
    PARK_ASSIST = 'PA'
    POWER_STEERING = 'PS'
    REVERSING_CAMERA = 'RC'
    AUTO_START_STOP = 'AS'

    FEATURE_CHOICES = (
        (CRUISE_CONTROL, 'Cruise Control'),
        (AUDIO_INTERFACE, 'Audio Interface'),
        (AIRBAGS, 'Airbags'),
        (AIR_CONDITIONING, 'Air Conditioning'),
        (SEAT_HEATING, 'Seat Heating'),
        (PARK_ASSIST, 'Park Assist'),
        (POWER_STEERING, 'Power Steering'),
        (REVERSING_CAMERA, 'Reversing Camera'),
        (AUTO_START_STOP, 'Auto Start/Stop'),
    )

    features = models.CharField(max_length=2, choices=FEATURE_CHOICES, blank=True)

    # A dunder method which is responsible for showing the Car name in the admin page
    def __str__(self):
        return self.car_name



# Definition of Buyer model which extends the User model
class Buyer(User):
    # A list of choices for the area field
    AREA_CHOICES = [
        ('W', 'Windsor'),
        ('LS', 'LaSalle'),
        ('A', 'Amherstburg'),
        ('L', 'Lakeshore'),
        ('LE', 'Leamington'),
        ('C', 'Chatham'),
        ('T', 'Toronto'),
        ('WA', 'Waterloo')
    ]

    # The field shipping_address of type CharField with a maximum length of 300
    # null and blank arguments are set to True meaning this field can be empty in the database and in forms
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    # The field area of type CharField with a maximum length of 2 and default value of 'C'
    # IV.	Change the default area value in the Buyer table from Windsor to Chatham
    area = models.CharField(max_length=2, choices=AREA_CHOICES, default='C')
    # III.	Add a phone number field in the Buyer table. The value of this field can be NULL.
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # The field interested_in of type ManyToManyField which references CarType model
    # This means each Buyer can be interested in many CarTypes and each CarType can be of interest to many Buyers
    interested_in = models.ManyToManyField(CarType)

    # Dunder method to replace the text which is shown in the admin page with the username
    # VI.	Write a __str__ method discussed in Lecture 4 for each model.
    def __str__(self):
        return self.username


# -_-_-_-_-_-_-_-_-_-_ Our new model named OrderVehicle -_-_-_-_-_-_-_-_-_-_-_-_-_-_
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


class LabMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    semester = models.IntegerField()
    personal_page = models.URLField()

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['first_name']