from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .models import CarDealer, DealerReview, CarModel, CarMake
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,post_request, get_dealer_by_id_from_cf, get_request

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return(render(request, 'djangoapp/about.html'))
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    return(render(request, 'djangoapp/contact.html'))



# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/signup.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/signup.html', context)




# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7abb23c6-e361-4090-9991-028f4fed05b0/dealership-package/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7abb23c6-e361-4090-9991-028f4fed05b0/dealership-package/dealership"
        dealer = get_dealer_by_id_from_cf(url, dealer_id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/7abb23c6-e361-4090-9991-028f4fed05b0/dealership-package/review"
        reviews = get_dealer_reviews_from_cf(review_url, id=dealer_id)
        if reviews:
            print(reviews[0].review)
            context["reviews"] = reviews
            reviews = reviews[0].review
        else:
            reviews = "Something went wrong"

        return HttpResponse(reviews)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...



def add_review(request, id):
    context = {}
    dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/7abb23c6-e361-4090-9991-028f4fed05b0/dealership-package/dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            review = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = username
            review["dealership"] = dealer["dealership"]
            review["id"] = id
            review["review"] = request.POST["content"]
            review["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    review["purchase"] = True
            review["purchase_date"] = request.POST["purchasedate"]
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = review
            review_post_url =  "https://us-south.functions.appdomain.cloud/api/v1/web/dd273e21-8af8-4608-b838-529759a65be4/dealership-package/post-reviews"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)