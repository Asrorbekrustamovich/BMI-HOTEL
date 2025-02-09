from rest_framework import generics
from .models import Role, UserInfo, UserRole, Room, Customer, Booking, History
from .serializers import (
    RoleSerializer, UserInfoSerializer, UserRoleSerializer,
    RoomSerializer, CustomerSerializer, BookingSerializer, HistorySerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .models import UserRole
from django.contrib.auth.models import User
from .serializers import UserSerializer
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# UserInfo Views
class UserInfoListCreateView(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class UserInfoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

# UserRole Views
class UserRoleListCreateView(generics.ListCreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

class UserRoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

# Room Views
class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# Customer Views
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Booking Views
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# History Views
class HistoryListView(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class HistoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Retrieve, Update, and Delete a User
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .models import UserInfo, UserRole

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserInfo, UserRole
from django.contrib.auth.models import User

class LoginView(APIView):
    def post(self, request):
        # Getting the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # # Check if both fields are provided
        # if not username or not password:
        #     return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Try to find the user by username
        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({"detail": "Invalid username."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the password matches (assuming passwords are stored as plain text)
        if user.password != password:
            return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)


        # Get UserInfo if exists
        try:
            user_info = UserInfo.objects.get(user=user)
        except UserInfo.DoesNotExist:
            user_info = None

        # Get the user's role
        user_role = UserRole.objects.filter(user=user).first()

        # Prepare the response data
        response_data = {
            'userid': user.id,
            'username': user.username,
            'role': user_role.role.name if user_role else None,
            'user_info': user_info.bio if user_info else None,
        }

        return Response(response_data, status=status.HTTP_200_OK)
