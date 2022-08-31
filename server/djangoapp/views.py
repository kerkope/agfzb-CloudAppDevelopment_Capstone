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
        url = "https://6dfaa0fe.us-south.apigw.appdomain.cloud/api/dealership"
        Get dealers from the URL
        print("Url", url)
        dealerships = get_dealers_from_cf(url)
        Concat all dealer's short name
        context["dealers"] = dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        Return a list of dealer short name
        return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://c8394781.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        #print(reviews)
        context['reviews'] = reviews
        context['dealer_id'] = dealer_id
        temp = []
        for i in reviews:
            if i.dealership == dealer_id:
                print(i.name)
                temp.append(i)
        context['reviews'] = temp
        return render(request, 'djangoapp/dealer_details.html', context)
        # return HttpResponse(reviews[dealer_id].sentiment)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    context["dealer_id"] = dealer_id
    review = dict()
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
            if request.user.is_authenticated:
                review['review'] = {}
                review['review']["time"] = datetime.utcnow().isoformat()
                review['review']["dealership"] = dealer_id
                review['review']["review"] = request.POST["review"]
                review['review']["purchase"] = request.POST["purchase"]
                review['review']['purchase_date'] = request.POST['purchase_date'] or "Nil"
                review['review']["car_model"] = request.POST["car_model"] or "Nil"
                review['review']["car_make"] = request.POST["car_make"] or "Nil"
                review['review']["car_year"] = request.POST["car_year"] or "Nil"

                userr = User.objects.get(username=request.user)
                review['review']['id'] = userr.id
                review['review']["name"] = userr.first_name + " " + userr.last_name

                url = "https://c8394781.us-south.apigw.appdomain.cloud/api/review"
                
                #json_payload = {}
                #json_payload['review'] = review
                
                post_request(url, review, dealerId=dealer_id)

                return redirect('djangoapp:dealer_details', context)