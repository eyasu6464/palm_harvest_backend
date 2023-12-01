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
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.sessions.models import Session
from django.conf import settings







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
    branch_name = data.get('branchname')

    # Check if the branch name already exists
    if Branch.objects.filter(branchname=branch_name).exists():
        return Response({'Message': 'Branch name already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # If the branch name doesn't exist, proceed with branch registration
    serializer = BranchSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Message': 'Branch Registered'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    # Get the authenticated user
    auth_user = request.user

    # Check if the user is active
    if not auth_user.is_active:
        return Response({'Message': 'Account is deactivated. Cannot change password.'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the old and new passwords from the request data
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    # Validate if both old and new passwords are provided
    if not old_password or not new_password:
        return Response({'Message': 'Both old and new passwords are required for the change.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the old password matches the current password
    if not auth_user.check_password(old_password):
        return Response({'Message': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    # Set the new hashed password for the user
    auth_user.set_password(new_password)
    
    # Save the changes
    auth_user.save()

    # Return a response
    return Response({'Message': 'Password changed successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def forgetPassword(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()

    if user:
        # Generate a password reset token
        token = default_token_generator.make_token(user)

        # Create a PasswordReset entry
        reset_data = {'user': user.id, 'token': token}
        serializer = PasswordResetSerializer(data=reset_data)
        if serializer.is_valid():
            serializer.save()

            # Send email with reset link
            current_site = get_current_site(request)
            domain = current_site.domain
            uid = urlsafe_base64_encode(force_bytes(user.id))
            reset_url = f'http://{domain}/reset-password/{uid}/{token}/'

            subject = 'Reset Your Password'
            message = str({'reset_url': reset_url})
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

            return Response({'Message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'Message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def resetPassword(request, uidb64, token):
    try:
        # Decode the UID and get the user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)

        # Check if the provided token is valid
        if default_token_generator.check_token(user, token):
            # Update the user's password
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()

            # Invalidate existing sessions
            Session.objects.filter(expire_date__gte=timezone.now(), session_data__contains=str(user.id)).delete()

            # Optionally, you may want to invalidate the token to ensure it can't be reused
            # password_reset_token = PasswordReset.objects.get(user=user)
            # password_reset_token.delete()
            return Response({'Message': 'Password reset successfully'}, status=status.HTTP_200_OK)        
        else:
            return Response({'Message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)