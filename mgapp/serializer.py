from pyexpat import model
from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    user =serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model =order
        fields = '__all__'




