from django.db import models
from django.utils.timezone import now
import datetime

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=20, primary_key=True)
    desc = models.TextField()
    def __str__(self):
        return "Name: " + self.name + "," \
                "Description: " + self.desc

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=20, primary_key=True)
    SUV = 'suv'
    SEDAN = 'sedan'
    WAGON = 'wagon'
    JEEP = 'jeep'
    TYPE_CHOICES = [
        (SUV, 'SUV'),
        (SEDAN, 'Sedan'),
        (WAGON, 'Wagon'),
        (JEEP, 'Jeep')
    ]
    model_type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    year = models.IntegerField(default=datetime.date.today().year) 
    
    def __str__(self):
        return  "Make: " + self.make.name + "," \
                "Name: " + self.name + "," \
                "Year: " + str(self.year) + "," \
                "Type: " + self.model_type + "," \
                "Dealer ID: " + str(self.dealer_id)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
    
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # Optional attributes
        self.purchase_date = ""
        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)