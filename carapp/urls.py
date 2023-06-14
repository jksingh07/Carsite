from django.urls import path
from . import views

app_name = 'carapp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('lab_members/', views.lab_members, name='lab_members'),
    path('<int:cartype_no>', views.cardetail, name='cardetail'),
]