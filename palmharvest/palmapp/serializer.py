from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name','is_active')

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields= '__all__'

class PalmUserSerializer(serializers.ModelSerializer):
    palmuser = AuthUserSerializer()
    branch = BranchSerializer()
    class Meta:
        model = PalmUser
        fields = ('palmuser', 'branch', 'user_type', 'address')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields= '__all__'

class PalmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalmDetail
        fields= '__all__'

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = '__all__'

class ManagerHarvesterUserSerializer(serializers.Serializer):
    harvesterid = serializers.IntegerField()
    full_name = serializers.SerializerMethodField()
    image_count = serializers.IntegerField()
    total_fruits_collected = serializers.IntegerField()
    start_date = serializers.DateTimeField(format="%Y-%m-%d")
    last_date = serializers.DateTimeField(format="%Y-%m-%d")

    def get_full_name(self, obj):
        return f"{obj['palmuser__first_name']} {obj['palmuser__last_name']}"