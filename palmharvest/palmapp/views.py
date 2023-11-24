from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User as AuthUser
from rest_framework.response import Response
from .serializer import *
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone

# Create your views here.

@api_view(['POST'])
def register(request):
    if not AuthUser.objects.filter(username=request.data.get('email')).exists():
        authuser = AuthUser.objects.create(
            first_name = request.data.get('first_name'),
            last_name = request.data.get('last_name'),
            username = request.data.get('email'),
            email = request.data.get('email'),
            password = make_password(request.data.get('password'))
        )
        users = PalmUser.objects.create(
            palmuser = authuser,
            user_type = request.data.get('user_type'),
            address = request.data.get('address'),
            branch_id = request.data.get('branch_id')
        )
        return Response({
                'Message':'User Registered'
                },
                status=status.HTTP_200_OK
            )
    else:
        return Response({
            'Message':'User already exists'
        })
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registerBranch(request):
    data = request.data
    serializer = BranchSerializer(data=data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadImage(request):
    image_obj = request.data.get("image")
    if not image_obj:
        return Response({"error":"Image is Required"}, status=status.HTTP_400_BAD_REQUEST)
    image_instance = Image.objects.create(
        harvesterid = request.user,
        imagepath=image_obj,
        image_created = datetime.now(),
        image_uploaded = datetime.now())
    image_instance.save()
    serializer = ImageSerializer(image_instance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userInfo(request):
    palmuser = PalmUser.objects.get(palmuser = request.user)
    serializer = PalmUserSerializer(palmuser)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allBranches(request):
    branch = Branch.objects.all()    
    serializer = BranchSerializer(branch, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allUsers(request):
    user = PalmUser.objects.all()    
    serializer = PalmUserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allimages(request):
    image = Image.objects.all()    
    serializer = ImageSerializer(image, many=True)
    return Response(serializer.data)