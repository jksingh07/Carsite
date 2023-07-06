from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import CarType, Vehicle, LabMember
from django.http import Http404
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

# Create your views here.
# def homepage(request):
#     cartype_list = CarType.objects.all().order_by('id')
#     response = HttpResponse()
#     heading1 = '<h1>' + 'Different types of Cars' + '</h1>'
#     response.write(heading1)
#
#     for cartype in cartype_list:
#         para = '<p>'+ ' '+ str(cartype.id) + ' '+ str(cartype) + '</p>'
#         response.write(para)
#
#     heading2 = '<h1>' + 'Different types of Vehicles' + '</h1>'
#     response.write(heading2)
#
#     vehicles_list = Vehicle.objects.all().order_by('car_price')[::-1][:10]
#
#     for vehicle in vehicles_list:
#         para = '<p>' +' '+ str(vehicle.id) + ' '+ str(vehicle) + ' '+ str(vehicle.car_price) + '</p>'
#         response.write(para)
#
#     return response
def homepage(request):
    cartype_list = CarType.objects.all().order_by('id')
    context = {
        'cartype_list': cartype_list
    }
    return render(request, 'homepage.html', context)
def aboutus(request):

    # response = HttpResponse()
    # heading1 = '<h1>' +' '+'This is a Car Showroom'+ '</h1>'
    # response.write(heading1)

    return render(request, 'aboutus.html')

# def cardetail(request, cartype_no):
#     response = HttpResponse()
#
#     try:
#         cartype = get_object_or_404(CarType, pk=cartype_no)
#
#     except Http404:
#         return render(request, '404.html')
#
#     all_cars_id = CarType.objects.values('id')
#     ids = [car['id'] for car in all_cars_id]
#     if cartype_no not in ids:
#         return render(request, '404.html')
#         response.write("Page Not Found")
#     else:
#         vehicles = Vehicle.objects.filter(car_type=cartype_no)
#         heading1 = '<h1> Car Details </h1>'
#         response.write(heading1)
#         heading2 = '<h2> Brand: '+ str(list(CarType.objects.filter(id=cartype_no))[0]) + '</h2>'
#         response.write(heading2)
#         columns = '<p> Car_Name  Brand  Price Inventory  Instock <p>'
#         response.write(columns)
#         for vehicle in vehicles:
#             para = '<p>' + ' '+ str(vehicle) +'&nbsp&nbsp&nbsp'+ str(vehicle.car_type) +'&nbsp&nbsp&nbsp'+ str(vehicle.car_price) +'&nbsp&nbsp&nbsp'+ str(vehicle.description) +'&nbsp&nbsp&nbsp'+ str(vehicle.inventory)+'&nbsp&nbsp&nbsp'+ str(vehicle.instock)+'</p>'
#             response.write(para)
#     return response

def cardetail(request, cartype_no):
    try:
        cartype = get_object_or_404(CarType, pk=cartype_no)
    except Http404:
        return render(request, '404.html')

    vehicles = Vehicle.objects.filter(car_type=cartype_no)

    context = {
        'cartype': cartype,
        'vehicles': vehicles,
    }

    return render(request, 'cardetail.html', context)
def lab_members(request):
    members = LabMember.objects.order_by('first_name')
    context = {
        'members': members
    }
    return render(request, 'lab_member.html', context)


# CLASS BASED VIEWS
class LabMembersView(View):
    def get(self, request):
        members = LabMember.objects.order_by('first_name')
        context = {
            'members': members
        }
        return render(request, 'lab_member.html', context)

class AboutUsView(View):
    def get(self, request):
        response = HttpResponse()
        heading1 = '<h1>' +' '+'This is a Car Showroom'+ '</h1>'
        response.write(heading1)
        return response

class Vehicles(View):
    def get(self, request):
        cars = Vehicle.objects.all()
        context={
            'cars':cars
        }
        return render(request, 'vehicles.html', context)

class OrderHere(View):
    def get(self, request):
        return render(request, 'orderhere.html', {})
# Differences noticed:
# - The FBV is a simple Python function that takes a request argument and returns a response.
# - The CBV is a class that inherits from the `View` class provided by Django.
# - In the FBV, the view logic is written directly in the function body.
# - In the CBV, the view logic is written in methods corresponding to HTTP methods (e.g., `get`, `post`, etc.).
# - In the FBV, the function name is used as the view's name when defining URL patterns.
# - In the CBV, the view is referenced as `MyView.as_view()` when defining URL patterns.
# - The CBV provides pre-defined methods for different HTTP methods that can be overridden as needed.
# - The CBV allows for easy reuse of common functionality by leveraging inheritance and mixins.
# - The CBV provides additional features like class-based decorators, mixins, and method-based dispatching.