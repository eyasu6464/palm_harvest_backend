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
from datetime import datetime
from django.utils import timezone
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import Http404
from django.db import transaction
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes








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
        return Response({"error": "Image is Required"}, status=status.HTTP_400_BAD_REQUEST)

    # Open the image using Pillow
    original_image = PILImage.open(image_obj)

    # Resize the image to 1280x1280 pixels
    resized_image = original_image.resize((1280, 1280))

    # Save the resized image to a BytesIO buffer
    image_buffer = BytesIO()
    resized_image.save(image_buffer, format='JPEG')

    # Create an InMemoryUploadedFile from the buffer
    uploaded_image = InMemoryUploadedFile(
        image_buffer,
        None,
        'image.jpg', 
        'image/jpeg',
        image_buffer.tell(),
        None
    )

    # Create and save the Image model instance
    image_instance = Image.objects.create(
        harvesterid=request.user,
        imagepath=uploaded_image,
        image_created=timezone.now(),
        image_uploaded=timezone.now()
    )

    # Save the image instance
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
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    branch = Branch.objects.all()    
    serializer = BranchSerializer(branch, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getbranch(request,pk):
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    branch = get_object_or_404(Branch, branchid=pk)
    serializer = BranchSerializer(branch, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allUsers(request):
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    user = PalmUser.objects.filter(user_type = "Harvester")    
    serializer = PalmUserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allimages(request):
    # Check if the authenticated user is a manager
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    images = Image.objects.all()
    serializer = ImageSerializer(images, many=True)

    # Enhance the serialized data by including image, harvester, and branch details
    serialized_data = []
    for image_data in serializer.data:
        # Fetch and serialize harvester information
        harvester_id = image_data['harvesterid']
        harvester = PalmUser.objects.get(pk=harvester_id)
        harvester_serializer = PalmUserSerializer(harvester)
        harvester_data = harvester_serializer.data

        # Fetch and serialize branch information
        branch_id = harvester.branch_id
        branch = Branch.objects.get(pk=branch_id)
        branch_serializer = BranchSerializer(branch)
        branch_data = branch_serializer.data

        # Parse string dates into datetime objects
        image_created = datetime.strptime(image_data['image_created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        image_uploaded = datetime.strptime(image_data['image_uploaded'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Format the date fields
        image_created_formatted = image_created.strftime('%Y-%m-%d')
        image_uploaded_formatted = image_uploaded.strftime('%Y-%m-%d')

        # Get PalmDetails associated with the image
        palmdetails = PalmDetail.objects.filter(imageid=image_data['imageid'])
        palmdetail_serializer = PalmDetailSerializer(palmdetails, many=True)

        # Create the final response data format
        response_data = {
            'imageid': image_data['imageid'],
            'imagepath': image_data['imagepath'],
            'image_created': image_created_formatted,
            'image_uploaded': image_uploaded_formatted,
            'harvester_id': harvester_data['palmuser']['id'],
            'harvester_fullname': f"{harvester_data['palmuser']['first_name']} {harvester_data['palmuser']['last_name']}",
            'branch_id': branch_data['branchid'],
            'branch_name': branch_data['branchname'],
            'branch_city': branch_data['city'],
            'palmdetails': palmdetail_serializer.data,
        }

        serialized_data.append(response_data)

    return Response(serialized_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def allBranchNames(request):
    branches = Branch.objects.all()
    data = [{'id': branch.branchid, 'name': branch.branchname} for branch in branches]
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inactiveUsers(request):
    inactive_users = AuthUser.objects.filter(is_active=False)
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
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
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
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
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
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
            reset_url = f'http://palmfrontend.blackneb.com/#/resetpassword/{uid}/{token}/'

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
        return Response({'Message': 'InvalidLink'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getImageDetails(request, pk):
    # Check if the authenticated user is a manager
    user_type = request.user.palmuser.user_type
    if user_type != 'Manager':
        return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # Get the image based on the provided ID
    image = get_object_or_404(Image, imageid=pk)

    # Serialize the image details
    image_serializer = ImageSerializer(image)

    # Get and serialize harvester information
    harvester_id = image_serializer.data['harvesterid']
    harvester = get_object_or_404(PalmUser, pk=harvester_id)
    harvester_serializer = PalmUserSerializer(harvester)
    harvester_data = harvester_serializer.data

    # Get and serialize branch information
    branch_id = harvester.branch_id
    branch = get_object_or_404(Branch, pk=branch_id)
    branch_serializer = BranchSerializer(branch)
    branch_data = branch_serializer.data

    # Parse string dates into datetime objects
    image_created = datetime.strptime(image_serializer.data['image_created'], '%Y-%m-%dT%H:%M:%S.%fZ')
    image_uploaded = datetime.strptime(image_serializer.data['image_uploaded'], '%Y-%m-%dT%H:%M:%S.%fZ')

    # Format the date fields
    image_created_formatted = image_created.strftime('%Y-%m-%d')
    image_uploaded_formatted = image_uploaded.strftime('%Y-%m-%d')

    # Get and serialize PalmDetail items associated with the image
    palmdetails = PalmDetail.objects.filter(imageid=image)
    palmdetail_serializer = PalmDetailSerializer(palmdetails, many=True)

    # Create the final response data format
    response_data = {
        'imageid': image_serializer.data['imageid'],
        'imagepath': image_serializer.data['imagepath'],
        'image_created': image_created_formatted,
        'image_uploaded': image_uploaded_formatted,
        'harvester_id': harvester_data['palmuser']['id'],
        'harvester_fullname': f"{harvester_data['palmuser']['first_name']} {harvester_data['palmuser']['last_name']}",
        'branch_id': branch_data['branchid'],
        'branch_name': branch_data['branchname'],
        'branch_city': branch_data['city'],
        'palmdetails': palmdetail_serializer.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)

from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendEmail(request):
    try:
        subject = request.data.get('subject')
        message = request.data.get('message')
        user_id = request.data.get('userid')

        # Ensure required fields are provided
        if not subject or not message or not user_id:
            return Response({'Message': 'Subject, message, and user ID are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get user email by ID
        try:
            user = User.objects.get(id=user_id)
            to_email = user.email
        except User.DoesNotExist:
            return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Send the email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)

        return Response({'Message': 'Email sent successfully.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'Message': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def palmDetailed(request):
    try:
        # Add any additional validation based on your requirements
        serializer = PalmDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Palm details entered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'Message': f'Error entering palm details: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteImage(request, pk):
    try:
        # Check if the authenticated user is a manager
        user_type = request.user.palmuser.user_type
        if user_type != 'Manager':
            return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        with transaction.atomic():
            # Get the image based on the provided ID
            image = get_object_or_404(Image, imageid=pk)

            # Delete all PalmDetail rows associated with the image
            PalmDetail.objects.filter(imageid=image).delete()

            # Delete the image
            image.delete()

        return Response({'Message': 'Image and associated PalmDetails deleted successfully'}, status=status.HTTP_200_OK)

    except Http404:
        return Response({'Message': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPalmDetail(request):
    try:
        # Extract data from the request
        data = request.data

        # Ensure the required fields are provided
        required_fields = ['quality', 'imageid', 'real', 'predicted', 'x1_coordinate', 'y1_coordinate', 'x2_coordinate', 'y2_coordinate']
        for field in required_fields:
            if field not in data:
                return Response({'Message': f'{field} is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the Image object based on the provided imageid
        image_id = data['imageid']
        image = get_object_or_404(Image, imageid=image_id)

        # Create the PalmDetail instance
        palm_detail = PalmDetail.objects.create(
            quality=data['quality'],
            imageid=image,
            real=data['real'],
            predicted=data['predicted'],
            x1_coordinate=data['x1_coordinate'],
            y1_coordinate=data['y1_coordinate'],
            x2_coordinate=data['x2_coordinate'],
            y2_coordinate=data['y2_coordinate'],
            palm_image_uploaded=timezone.now()
        )

        # Serialize and return the created PalmDetail instance
        serializer = PalmDetailSerializer(palm_detail)
        return Response({'Message': 'Coordinate created successfully.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'Message': f'Error creating PalmDetail: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePalmDetail(request, pk):
    try:
        # Check if the authenticated user is a manager or has appropriate permissions
        # Adjust the permission check based on your requirements
        user_type = request.user.palmuser.user_type
        if user_type != 'Manager':
            return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the PalmDetail object based on the provided ID
        palm_detail = get_object_or_404(PalmDetail, palmid=pk)

        # Delete the PalmDetail
        palm_detail.delete()

        return Response({'Message': 'PalmDetail deleted successfully.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'Message': f'Error deleting PalmDetail: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)