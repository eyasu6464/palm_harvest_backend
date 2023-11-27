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
            password = make_password(request.data.get('password')),
            is_active=False
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
        },
        status=status.HTTP_400_BAD_REQUEST)
        
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
def getbranch(request,pk):
    branch = get_object_or_404(Branch, branchid=pk)
    serializer = BranchSerializer(branch, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allUsers(request):
    user = PalmUser.objects.filter(palmuser__is_active = True)    
    serializer = PalmUserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allimages(request):
    image = Image.objects.all()    
    serializer = ImageSerializer(image, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def allBranchNames(request):
    branches = Branch.objects.all()
    data = [{'id': branch.branchid, 'name': branch.branchname} for branch in branches]
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inactiveUsers(request):
    inactive_users = AuthUser.objects.filter(is_active=False)
    
    user_data = []
    for user in inactive_users:
        user_info = {
            'userid': user.id,
            'username': user.username,
            'firstname': user.first_name,
            'lastname': user.last_name
        }
        user_data.append(user_info)
    
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activateAccount(request, id):
    try:
        user = AuthUser.objects.get(id=id)
    except AuthUser.DoesNotExist:
        return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.is_active = True
    user.save()

    return Response({'Message': 'User account activated successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivateAccount(request, id):
    try:
        user = AuthUser.objects.get(id=id)
    except AuthUser.DoesNotExist:
        return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.is_active = False
    user.save()

    return Response({'Message': 'User account deactivated successfully'}, status=status.HTTP_200_OK)