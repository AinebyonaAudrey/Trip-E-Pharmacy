from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Prescription

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('file',)