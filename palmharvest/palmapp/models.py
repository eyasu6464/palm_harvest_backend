from django.db import models
from django.contrib.auth.models import User as AuthUser


class UserType(models.TextChoices):
    Admin = 'Admin'
    Manager = 'Manager'
    Harvester = 'Harvester'

class Branch(models.Model):
    branchid = models.AutoField(primary_key=True)
    branchname = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address_longitude = models.CharField(max_length=50)
    address_latitude = models.CharField(max_length=50)

class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, 
                                 choices=UserType.choices, 
                                 default=UserType.Harvester)
    address = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    

class Image(models.Model):
    imageid = models.AutoField(primary_key=True)
    harvesterid = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    image_created = models.DateTimeField()
    image_uploaded = models.DateTimeField()
    
class PalmDetail(models.Model):
    palmid = models.AutoField(primary_key=True)
    quality = models.CharField(max_length=50)
    imageid = models.ForeignKey(Image, on_delete=models.CASCADE)
    real = models.CharField(max_length=50)
    predicted = models.BooleanField()
    x1_coordinate = models.CharField(max_length=50)
    y1_coordinate = models.CharField(max_length=50)
    x2_coordinate = models.CharField(max_length=50)
    y2_coordinate = models.CharField(max_length=50)
    palm_image_uploaded = models.DateTimeField()
