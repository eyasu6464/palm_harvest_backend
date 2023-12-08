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

class PalmUser(models.Model):
    palmuser = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, 
                                 choices=UserType.choices, 
                                 default=UserType.Harvester)
    address = models.CharField(max_length=50)    

class Image(models.Model):
    imageid = models.AutoField(primary_key=True)
    harvesterid = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    imagepath = models.FileField(upload_to='uploads/')
    image_created = models.DateTimeField()
    image_uploaded = models.DateTimeField()
    
class PalmDetail(models.Model):
    palmid = models.AutoField(primary_key=True)
    quality = models.CharField(max_length=50)
    imageid = models.ForeignKey(Image, on_delete=models.CASCADE)
    real = models.BooleanField()
    predicted = models.BooleanField()
    x1_coordinate = models.CharField(max_length=50)
    y1_coordinate = models.CharField(max_length=50)
    x2_coordinate = models.CharField(max_length=50)
    y2_coordinate = models.CharField(max_length=50)
    palm_image_uploaded = models.DateTimeField()

class PasswordReset(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
