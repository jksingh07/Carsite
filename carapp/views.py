from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import CarType, Vehicle, LabMember
from django.http import Http404
# Create your views here.
def homepage(request):
    cartype_list = CarType.objects.all().order_by('id')
    response = HttpResponse()
    heading1 = '<h1>' + 'Different types of Cars' + '</h1>'
    response.write(heading1)

    for cartype in cartype_list:
        para = '<p>'+ ' '+ str(cartype.id) + ' '+ str(cartype) + '</p>'
        response.write(para)

    heading2 = '<h1>' + 'Different types of Vehicles' + '</h1>'
    response.write(heading2)

    vehicles_list = Vehicle.objects.all().order_by('car_price')[:10]

    for vehicle in vehicles_list:
        para = '<p>' +' '+ str(vehicle.id) + ' '+ str(vehicle) + ' '+ str(vehicle.car_price) + '</p>'
        response.write(para)

    return response

def aboutus(request):

    response = HttpResponse()
    heading1 = '<h1>' +' '+'This is a Car Showroom'+ '</h1>'
    response.write(heading1)

    return response

def cardetail(request, cartype_no):
    response = HttpResponse()

    try:
        cartype = get_object_or_404(CarType, pk=cartype_no)

    except Http404:
        return render(request, '404.html')

    all_cars_id = CarType.objects.values('id')
    ids = [car['id'] for car in all_cars_id]
    if cartype_no not in ids:
        return render(request, '404.html')
        response.write("Page Not Found")
    else:
        vehicles = Vehicle.objects.filter(car_type=cartype_no)
        heading1 = '<h1> Car Details </h1>'
        response.write(heading1)
        heading2 = '<h2> Brand: '+ str(list(CarType.objects.filter(id=cartype_no))[0]) + '</h2>'
        response.write(heading2)
        columns = '<p> Car_Name  Brand  Price Inventory  Instock <p>'
        response.write(columns)
        for vehicle in vehicles:
            para = '<p>' + ' '+ str(vehicle) +'&nbsp&nbsp&nbsp'+ str(vehicle.car_type) +'&nbsp&nbsp&nbsp'+ str(vehicle.car_price) +'&nbsp&nbsp&nbsp'+ str(vehicle.description) +'&nbsp&nbsp&nbsp'+ str(vehicle.inventory)+'&nbsp&nbsp&nbsp'+ str(vehicle.instock)+'</p>'
            response.write(para)
    return response

def lab_members(request):
    members = LabMember.objects.order_by('first_name')
    context = {
        'members': members
    }
    return render(request, 'lab_member.html', context)
