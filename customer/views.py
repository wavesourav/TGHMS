import math
from wsgiref.util import request_uri
from django.shortcuts import render, get_object_or_404
import customer
from django.contrib import messages
from customer.models import Customer, Orders
from restaurant.models import FoodItem, Restaurant
from manager.models import Station, Train
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

import json
# Create your views here.

# login functions
def login(request):
    return render(request, 'customer/index.html')

def login_customer(request):
    obj = None
    for customer in Customer.objects.all():
        if customer.username == request.POST['username'] and customer.password == request.POST['password'] and customer.username!= "" and customer.password!= "":
            obj = customer
            break
    
    if obj is None:
        messages.error(request, 'Invalid Credentials!')
        return HttpResponseRedirect('../login/', status=302)

    return HttpResponseRedirect('../dashboard/' + str(obj.id))

# register functions
def register(request):
    return render(request, 'customer/register.html')

def register_customer(request):
    if request.POST['password'] == request.POST['re_password'] and request.POST['password']!= "" and request.POST['username']!= "" : 
        customer = Customer(username= request.POST['username'], password= request.POST['password'], phone_number = request.POST['phone_number'])

        if Customer.objects.filter(username=customer.username, password = customer.password, phone_number = customer.phone_number).exists():
            return HttpResponseRedirect('../dashboard/' + str(Customer.objects.filter(username=customer.username, password = customer.password)[0].id))
        
        customer.save()
        return HttpResponseRedirect('../dashboard/' + str(customer.id))
    else: 
        messages.error(request, 'Invalid username, mobile number or passwords do not match!')
        return HttpResponseRedirect('../register/', status = 302)

# function to display the dashboard
def dashboard(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    order_list  = Orders.objects.filter(customer=customer)
    context = {'order_list': order_list, 'customer': customer, 'train_list': Train.objects.all(), 'food_list': FoodItem.objects.all()}
    return render(request, 'customer/dashboard.html', context)

# function to fetch the station list and restaurant list corresponding to the train
def fetch_station(request):
    station = Train.objects.get(id=request.GET['train_id']).stations.split(' ')
    station_list, id_list = [],[]
    for i in station:
        id_list.append(i)
        station_list.append(Station.objects.get(id=i).name)

    restaurant_list = []
    

    for id in id_list:
        res_list = Restaurant.objects.filter(station=id)

        for res in  res_list:
            if res.id is not None:
                restaurant_list.append([res.id, res.name])
    

    return JsonResponse({'station_list': station_list, 'id_list': id_list, 'restaurant_list': restaurant_list})

# function to fetch the food item list corresponding to the selected restaurant
def fetch_food(request):
    restaurant = Restaurant.objects.get(id=request.GET['restaurant_id'])
    food_list = FoodItem.objects.filter(restaurant=restaurant)

    foods = []

    for food in food_list:
        foods.append([food.id, food.name, food.price])

    return JsonResponse({'food_list': foods})

# function to get the travel-time of delivery

def get_time(request):

    food = FoodItem.objects.get(id=request.GET['food_id'])

    time=food.f_time
    hr = int(time//60)
    min = int((time - hr*60) )
    sec = int(0)

    return JsonResponse({'time': str(hr) + " hr : " + str(min) + " min : " + str(sec) + " sec"})

# function to place an order
def place_order(request,customer_id):
    order = Orders(customer = Customer.objects.get(id=customer_id), restaurant = Restaurant.objects.get(id=request.POST['restaurant']), food_item = request.POST['food'],plates = request.POST['plates'])
    order.save()

    return HttpResponseRedirect('../dashboard/' + str(customer_id))

def change_status(request,order_id):
    order = Orders.objects.get(id=order_id)
    order.status += 1
    order.save()
    return HttpResponseRedirect('../dashboard/' + str(order.customer.id))