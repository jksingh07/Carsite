from django.urls import path
from . import views
from .views import LabMembersView, AboutUsView, Vehicles, OrderHereView, SearchView, HomepageView

app_name = 'carapp'
urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('', HomepageView.as_view(), name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('about/', AboutUsView.as_view(),name='AboutUsView'),
    path('lab_members/', views.lab_members, name='lab_members'),
    path('LabMembers/', LabMembersView.as_view(), name='LabMembers'),
    path('<int:cartype_no>', views.cardetail, name='cardetail'),
    path('vehicles/', Vehicles.as_view(), name='Vehicles'),
    path('order/', OrderHereView.as_view(), name='OrderHere'),
    path('search/', SearchView.as_view(), name='search'),
    path('login_here/', views.login_here, name='login_here'),
    path('logout_here/', views.logout_here, name='logout_here'),
    path('list_of_orders/', views.list_of_orders, name='list_of_orders'),
    path('sign_up/', views.sign_up, name='sign_up'),
]