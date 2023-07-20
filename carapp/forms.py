from django import forms
from .models import OrderVehicle
from django.contrib.auth.forms import UserCreationForm
from .models import Buyer
class OrderVehicleForm(forms.ModelForm):
    class Meta:
        model = OrderVehicle
        fields = ['vehicle', 'buyer', 'quantity']
        labels = {
            'vehicle': 'Vehicle',
            'buyer': 'Buyer',
            'quantity': 'Number of Vehicles Ordered'
        }
        widgets = {
            'buyer': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class':'form-control'}),
        }
class BuyerCreationForm(UserCreationForm):
    shipping_address = forms.CharField(max_length=300, required=False)
    area = forms.ChoiceField(choices=Buyer.AREA_CHOICES, initial='C')
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = UserCreationForm.Meta.fields + ('shipping_address', 'area', 'phone_number', 'interested_in')
class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Subject', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Message', required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))