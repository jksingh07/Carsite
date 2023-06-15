from django.urls import path
from . import views
from .views import LabMembersView, AboutUsView

app_name = 'carapp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('about/', AboutUsView.as_view(),name='AboutUsView'),
    path('lab_members/', views.lab_members, name='lab_members'),
    path('LabMembers/', LabMembersView.as_view(), name='LabMembers'),
    path('<int:cartype_no>', views.cardetail, name='cardetail'),
]