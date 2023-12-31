from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.views import View
from .forms import OrderVehicleForm, ContactForm, BuyerCreationForm
from .models import CarType, Vehicle, LabMember, OrderVehicle
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
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

def login_here(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return HttpResponseRedirect(reverse('carapp:homepage'))
            else:
                return HttpResponse("Your Account is Disabled")
        else:
            return HttpResponse("Incorrect login details")
    else:
        return render(request, 'login_here.html')

@login_required
def logout_here(request):
    # Log the user out and redirect to the homepage
    logout(request)
    return HttpResponseRedirect(reverse('carapp:homepage'))


@login_required
def list_of_orders(request):
    # Check if the user is a buyer
    # print("here")
    user = request.user
    if request.user.is_authenticated:
        request.session.set_expiry(settings.EXPIRY_LIMIT)
        request.session['session_expired_message'] = 'Your Session is Expired, Login Again'
        # # Clear the message from the session after displaying it
        # if 'session_expired_message' in request.session:
        #     del request.session['session_expired_message']
    if hasattr(user, 'buyer'):
        # Get all orders placed by the user
        orders = OrderVehicle.objects.filter(buyer=request.user)
        # Render the list of orders template with the orders
        print(orders)
        return render(request, 'list_of_orders.html', {'orders': orders})
    else:
        # Return a message if the user is not a buyer
        return render(request, 'list_of_orders.html', {'message': 'You are not registered'})


def sign_up(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = BuyerCreationForm(request.POST)
        if form.is_valid():
            print("Valid Form Data")
            form.save()
            # Redirect to a success page or the homepage
            return redirect('carapp:homepage')  # Change 'home' to the name of your homepage URL pattern
        else:
            print("Invalid Form Data")
    else:
        # form = UserCreationForm()
        form = BuyerCreationForm()

    return render(request, 'sign_up.html', {'form': form})
# def homepage(request):
#     cartype_list = CarType.objects.all().order_by('id')
#     context = {
#         'cartype_list': cartype_list
#     }
#     return render(request, 'homepage.html', context)


class HomepageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            request.session.set_expiry(settings.EXPIRY_LIMIT)
            request.session['session_expired_message'] = 'Your Session is Expired, Login Again'
            # # Clear the message from the session after displaying it
            # if 'session_expired_message' in request.session:
            #     del request.session['session_expired_message']

        cartype_list = CarType.objects.all().order_by('id')
        # Pass the cartype_list variable as context to the 'homepage.html' template
        session_count = request.session.get('session_count', 0)
        session_count += 1
        request.session['session_count'] = session_count
        context = {
            'cartype_list': cartype_list,
            'session_count': session_count,
        }
        return render(request, 'homepage.html', context)

def aboutus(request):
    if request.user.is_authenticated:
        request.session.set_expiry(settings.EXPIRY_LIMIT)
        request.session['session_expired_message'] = 'Your Session is Expired, Login Again'
        # # Clear the message from the session after displaying it
        # if 'session_expired_message' in request.session:
        #     del request.session['session_expired_message']
    session_count = request.session.get('session_count', 0)
    session_count+=1
    request.session['session_count'] = session_count
    response = render(request, 'aboutus.html', {'session_count': session_count})
    response.set_cookie('counter', 10, max_age=10)
    return response

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

class OrderHereView(View):
    def get(self, request):
        msg = ''
        vehiclelist = Vehicle.objects.all()
        form = OrderVehicleForm()
        return render(request, 'orderhere.html', { 'form': form, 'msg': msg, 'vehiclelist': vehiclelist})

    def post(self, request):
        msg = ''
        vehiclelist = Vehicle.objects.all()
        form = OrderVehicleForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.quantity <= order.vehicle.inventory:
                order.vehicle.inventory -= order.quantity
                order.vehicle.save()
                order.status = 1
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fulfill your order.'
                return render(request, 'nosuccess_order.html', {'msg': msg})
        else:
            msg = 'There was an error with your order. Please try again.'

        return render(request, 'orderhere.html', {'form': form, 'msg': msg, 'vehiclelist': vehiclelist})

class SearchView(View):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        context = {
            'vehicles': vehicles
        }
        return render(request, 'search.html', context)

    def post(self, request):
        vehicles = Vehicle.objects.all()
        selected_vehicle_id = request.POST.get('selected_vehicle')
        selected_vehicle = get_object_or_404(Vehicle, pk=selected_vehicle_id)
        return render(request, 'search.html', {'vehicles': vehicles,'selected_vehicle': selected_vehicle})

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