from django.http import HttpResponseRedirect, HttpResponse
from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import View
from django.urls import reverse_lazy
from django import forms
from django.views import generic
from .restapi import get_dealers_from_cf 
#from .models import related models
#from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)
  
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html' 

class ReviewPageView(TemplateView):
    template_name = 'reviews.html'

class ContactPageView(TemplateView):
    template_name = 'contact.html' 

class SignupPageView(TemplateView):
    template_name = 'signup.html' 

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('/')

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('/')
        else:
            # If not, return to login page again
            return render(request, 'signup.html', context)
    else:
        return render(request, '/', context)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

def register(request):
    if request.method == 'GET':
        form  = RegisterForm()
        context = {'form': form}
        return render(request, 'signup.html', context)
    if request.method == 'POST':
        form  = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + user)
        return redirect('/')
    else:
        print('Form is not valid')
        messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'signup.html', context)
        return render(request, 'signup.html', {})


def get_dealerships(request):

    if request.method == "GET":
        context = {}
        context=dict()
        url = "https://6dfaa0fe.us-south.apigw.appdomain.cloud/api/dealership"
        
        # Get dealers from the URL

        dealerships, result = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        context["result"] = result
        
        # Return a list of dealer short name
        return render(request, 'djangoapp/home.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, id):
# View to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://6dfaa0fe.us-south.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
    
        review_url = "https://6dfaa0fe.us-south.apigw.appdomain.cloud/api/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/reviews.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
# View to submit a new review
def add_review(request, id):
    context = {}
    dealer_url = "https://6dfaa0fe.us-south.apigw.appdomain.cloud/api/dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/reviews.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://6dfaa0fe.us-south.apigw.appdomain.cloud/api/post-review"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)     