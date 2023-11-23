from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields= '__all__'

class PalmUserSerializer(serializers.ModelSerializer):
    palmuser = AuthUserSerializer()
    class Meta:
        model = PalmUser
        fields = ('palmuser', 'branch', 'user_type', 'address', 'status')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields= '__all__'

class PalmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalmDetail
        fields= '__all__'
