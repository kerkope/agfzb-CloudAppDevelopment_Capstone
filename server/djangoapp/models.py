from django.db import models
from django.utils.timezone import now
from django.core import serializers 
import uuid
import json

class CarMake(models.Model):
    name = models.CharField(null= False, max_length=30)
    description = models.CharField(null= False, max_length=300)

    def __str__(self):
        return 'Name:' + self.name + ',' + \
            'Description:' + self.description


class CarModel(models.Model):
    TYPES = (
            ("SEDAN", "Sedan"), ("SUV", "SUV"), ("WAGON", "Wagon"), ("LIMOUSINE", "Limousine"), ("BATMOBILE", "Batmobile")
        )
    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)  
    name = models.CharField(null=False, max_length=30)
    c_type = models.CharField(max_length=30, choices=TYPES)
    dealer_id = models.IntegerField()
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + \
                " Make Name: "+ self.make.name + \
                " Type: " + self.c_type + \
                " Dealer ID: " + str(self.dealer_id)+ \
                " Year: " + str(self.year)

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

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year,sentiment, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment 
        self.id=id

    def __str__(self):
        return "Review: " + self.review +\
                " Sentiment: " + self.sentiment

class ReviewPost:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year,sentiment, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment 
        self.id=id

    def __str__(self):
        return "Review: " + self.review +\
                " Sentiment: " + self.sentiment