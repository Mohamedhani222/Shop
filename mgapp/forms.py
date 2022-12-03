from dataclasses import fields
from pyexpat import model
from django import forms
from .models import *

class productsform(forms.ModelForm):

    class Meta:
        model =product
        fields = '__all__'
        exclude = ['createdat']
        
class respform(forms.ModelForm):
    class Meta:
        model =Responseticket
        fields='__all__'
