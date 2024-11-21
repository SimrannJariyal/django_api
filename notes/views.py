from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .models import User
from .serializers import LoginSerializer, UserProfileSerializer, RegisterSerializer
from rest_framework import viewsets
from .models import Subject, Unit
from .serializers import SubjectSerializer, UnitSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
import os
from django.conf import settings

# Login API View
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Use Django's authenticate method, it will handle the hashed password comparison
        user = authenticate(email=email, password=password)

        if user is not None:
            # If user is authenticated, generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'user_id': user.id  # Include user ID in the response
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Subject & Unit API ViewSets
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    @action(detail=True, methods=['get'], url_path='units')
    def units_by_subject(self, request, pk=None):
        subject = get_object_or_404(Subject, pk=pk)
        units = subject.units.all()
        serializer = UnitSerializer(units, many=True, context={'request': request})
        return Response(serializer.data)

# Logout API View
@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
    except TokenError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except InvalidToken as e:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

# User Registration API View
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Profile API View
@api_view(['GET'])
def user_profile(request, id):
    try:
        user = User.objects.get(id=id)
        if user.profile_photo:
            user.profile_photo_url = request.build_absolute_uri(settings.MEDIA_URL + str(user.profile_photo))
        else:
            user.profile_photo_url = None
        
        serializer = UserProfileSerializer(user)
        data = serializer.data
        data['profile_photo_url'] = user.profile_photo_url
        return Response(data)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

# Update Profile API View
@api_view(['PUT', 'PATCH'])
def update_profile(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import User

@api_view(['PUT'])
@parser_classes([MultiPartParser])
def update_profile_photo(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if 'profile_photo' in request.FILES:
        user.profile_photo = request.FILES['profile_photo']
        user.save()
        return Response({"message": "Profile photo updated successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "No photo provided"}, status=status.HTTP_400_BAD_REQUEST)

