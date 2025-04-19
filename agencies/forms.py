from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Agency, Resource

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    agency = forms.ModelChoiceField(queryset=Agency.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'agency', 'password1', 'password2']

class AgencyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'description', 'contact_email', 'contact_phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'contact_email': forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'contact_phone': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['agency', 'name', 'quantity', 'description']
        widgets = {
            'agency': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
        }
