from rest_framework import generics
from .models import Role, Bio, UserRole, Room, Customer, Booking,Status,Message,Department,Roomtype
from .serializers import (
    RoleSerializer, UserInfoSerializer, UserRoleSerializer,
    RoomSerializer, CustomerSerializer, BookingSerializer,StatusSerializer,MessageSerializer,DepartmentSerializer,RoomTypeSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .models import UserRole
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.exceptions import NotFound
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Bio
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoomTypeListCreateView(generics.ListCreateAPIView):
    queryset=Roomtype.objects.all()
    serializer_class=RoomTypeSerializer

class RoomTypeDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Roomtype.objects.all()
    serializer_class=RoomTypeSerializer  

class UserInfoFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Bio
        fields = ['user_id']
# UserInfo Views
class UserInfoListCreateView(generics.ListCreateAPIView):
    queryset = Bio.objects.all()
    serializer_class = UserInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserInfoFilter

class UserInfoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   serializer_class = UserInfoSerializer
   def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            return Bio.objects.get(user__id=user_id)
        except Bio.DoesNotExist:
            raise NotFound("UserInfo with the specified user_id does not exist.")

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

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class StatusListCreateView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = CustomerSerializer   


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Retrieve, Update, and Delete a User
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message, User
from .serializers import MessageSerializer

class MessageExchangeView(APIView):
    def get(self, request, *args, **kwargs):
        # Extract sender_id and receiver_id from kwargs
        sender_id = kwargs.get('sender_id')
        receiver_id = kwargs.get('receiver_id')

        # Get sender and receiver users
        sender = get_object_or_404(User, id=sender_id)
        receiver = get_object_or_404(User, id=receiver_id)

        # Fetch all messages sent by the sender to the receiver
        sent_messages = Message.objects.filter(sender=sender, receiver=receiver)

        # Fetch all messages sent by the receiver to the sender
        received_messages = Message.objects.filter(sender=receiver, receiver=sender)

        # Combine all messages between the two users
        all_messages = sent_messages.union(received_messages).order_by("timestamp")

        # If no messages exist, return a 404 response
        if not all_messages.exists():
            return Response(
                {"message": "No messages found between these users."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Mark only the messages sent by the receiver to the sender as read
        received_messages.update(is_read=True)

        # Serialize and return all messages
        serializer = MessageSerializer(all_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        # Getting the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if both fields are provided
        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Try to find the user by username
        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({"detail": "Invalid username."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the password matches (assuming passwords are stored as plain text)
        if user.password != password:
            return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)


        # Get UserInfo if exists
        try:
            user_info = Bio.objects.get(user=user)
        except Bio.DoesNotExist:
            user_info = None

        # Get the user's role
        user_role = UserRole.objects.filter(user=user).first()

        # Prepare the response data
        response_data = {
            'userid': user.id,
            'username': user.username,
            'role': user_role.role.name if user_role else None,
            'user_info': user_info. bio_text if user_info else None,
        }

        return Response(response_data, status=status.HTTP_200_OK)
