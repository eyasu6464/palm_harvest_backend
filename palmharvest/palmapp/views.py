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
        return Response({
                'Message':'Branch Registered'
                }, status=201)
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
    user = PalmUser.objects.filter(user_type = "Harvester")    
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activateAccount(request, id):
    try:
        user = AuthUser.objects.get(id=id)
    except AuthUser.DoesNotExist:
        return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.is_active = True
    user.save()

    return Response({'Message': 'User account activated successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deactivateAccount(request, id):
    try:
        user = AuthUser.objects.get(id=id)
    except AuthUser.DoesNotExist:
        return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.is_active = False
    user.save()

    return Response({'Message': 'User account deactivated successfully'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateBranch(request, pk):
    # Check if the current user is a manager
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the branch with the given primary key exists
    branch = get_object_or_404(Branch, pk=pk)

    # Check if the new branch name already exists
    new_branch_name = request.data.get('branchname')
    if Branch.objects.exclude(pk=pk).filter(branchname=new_branch_name).exists():
        return Response({'Message': 'Branch name already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the branch data
    serializer = BranchSerializer(branch, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Message': 'Branch updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBranch(request, pk):
    # Check if the current user is a manager
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the branch with the given primary key exists
    branch = get_object_or_404(Branch, pk=pk)

    # Delete the branch
    branch.delete()

    return Response({'Message': 'Branch deleted successfully'}, status=status.HTTP_200_OK)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    # Get the authenticated user
    auth_user = request.user

    # Check if the user is active
    if not auth_user.is_active:
        return Response({'Message': 'Account is deactivated'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the PalmUser associated with the authenticated user
    palm_user = get_object_or_404(PalmUser, palmuser=auth_user)

    # Update the user's profile
    auth_user.first_name = request.data.get('first_name', auth_user.first_name)
    auth_user.last_name = request.data.get('last_name', auth_user.last_name)
    auth_user.email = request.data.get('email', auth_user.email)

    # Update the PalmUser fields
    palm_user.user_type = request.data.get('user_type', palm_user.user_type)
    palm_user.address = request.data.get('address', palm_user.address)
    palm_user.branch_id = request.data.get('branch_id', palm_user.branch_id)

    # Save the changes
    auth_user.save()
    palm_user.save()

    # Return a response
    return Response({'Message': 'User profile updated successfully'}, status=status.HTTP_200_OK)