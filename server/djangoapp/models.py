from django.db import models
from django.utils.timezone import now
import datetime
import uuid
import json

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length= 50)
    description = models.TextField(null=True)
    def __str__(self):
        return self.name

######################################################################################################################

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    BIKE = "Bike"
    OTHER = "Other"
    CAR_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (BIKE, "Bike"),
        (OTHER, "Other")
    ]

    YEAR_CHOICES = []
    for r in range(1969, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r, r))

    make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    id = models.IntegerField(default=1, primary_key=True)
    model_type = models.CharField(null=False, max_length=15, choices=CAR_CHOICES, default=SEDAN)
    year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return self.name + ", " + str(self.year) + ", " + self.model_type



# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:

    def __init__(self, address, city, full_name, dealer_id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.dealer_id = dealer_id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, review_id, dealer_id, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.review_id = review_id
        self.dealer_id = dealer_id
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment