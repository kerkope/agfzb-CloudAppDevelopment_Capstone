import json
import logging
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import CarDealer, CarMake, CarModel
from .restapis import (get_dealer_by_id, get_dealer_reviews_from_cf, get_dealers_from_cf, post_request)

logger = logging.getLogger(__name__)

def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', {})

def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', {})

def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

def logout(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

def registration(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
                )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

def get_dealerships(request):
    if request.method == "GET":
        context = {}
        context['dealership_list'] = get_dealers_from_cf()
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        context['reviews'] = get_dealer_reviews_from_cf(dealer_id)
        context['dealer'] = get_dealer_by_id(dealer_id)
        return render(request, 'djangoapp/dealer_details.html', context)

@csrf_exempt
def add_review(request, dealer_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            review = {}
            form = request.POST
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = form.get('content', '')
            if form.get('purchasecheck', 'off') == 'on':
                review["purchase"] = True
            else:
                review["purchase"] = False
            review["purchase_date"] = form.get("purchasedate", "01/01/1970")
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
            review["name"] = request.user.username
            payload = {'review': review}
            add_response = post_request(URL_API+'/review', json_payload=payload)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            response = HttpResponse('You need to authenticate!')
            response.status_code = 401
            return response
    elif request.method == "GET":
        context = {}
        context['cars'] = list(CarModel.objects.filter(dealer_id = dealer_id))
        context['dealer'] = get_dealer_by_id(dealer_id)
        return render(request, 'djangoapp/add_review.html', context)