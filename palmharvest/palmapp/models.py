from django.db import models
from django.contrib.auth.models import User as AuthUser


class Branch(models.Model):
    branchid = models.IntegerField(primary_key=True)
    branchname = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address_longitude = models.CharField(max_length=50)
    address_latitude = models.CharField(max_length=50)

class User(models.Model):
    userid = models.IntegerField(primary_key=True)
    branchid = models.ForeignKey(Branch, on_delete=models.CASCADE)
    mainid = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    

class Image(models.Model):
    imageid = models.IntegerField(primary_key=True)
    harvester = models.ForeignKey(User, on_delete=models.CASCADE)
    image_created = models.DateTimeField()
    image_uploaded = models.DateTimeField()

class PalmDetail(models.Model):
    palmid = models.IntegerField(primary_key=True)
    quality = models.CharField(max_length=50)
    imageid = models.ForeignKey(Image, on_delete=models.CASCADE)
    real = models.CharField(max_length=50)
    predicted = models.BooleanField()
    x1_coordinate = models.CharField(max_length=50)
    y1_coordinate = models.CharField(max_length=50)
    x2_coordinate = models.CharField(max_length=50)
    y2_coordinate = models.CharField(max_length=50)
    palm_image_uploaded = models.DateTimeField()
