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
from .models import Bio, Message, Department, User
from .serializers import MessageSerializer

class WorkerSendMessageToManagerView(APIView):
    def post(self, request, user_id):
        # Get the worker's Bio
        worker_bio = get_object_or_404(Bio, user_id=user_id)

        # Ensure the worker has a department
        if not worker_bio.department:
            return Response(
                {"error": "Worker does not belong to any department."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find the manager in the same department
        manager_bio = Bio.objects.filter(
            department=worker_bio.department,
            position="Manager"  # Assuming "Manager" is the position title for managers
        ).first()

        if not manager_bio:
            return Response(
                {"error": "No manager found in the same department."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get the message content from the request
        content = request.data.get("content")
        if not content:
            return Response(
                {"error": "Message content is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the message
        message = Message.objects.create(
            sender=worker_bio.user,
            receiver=manager_bio.user,
            content=content
        )

        # Serialize the message and return the response
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class MessageList_beetween_manager_and_workers_View_For_manager(APIView):
    def get(self, request, sender_id, receiver_id):
        # Foydalanuvchilarni olish
        sender = get_object_or_404(User, id=sender_id)
        receiver = get_object_or_404(User, id=receiver_id)

        # Sender va receiver o‘rtasidagi barcha xabarlarni olish
        sent_messages = Message.objects.filter(sender=sender, receiver=receiver)
        received_messages = Message.objects.filter(sender=receiver, receiver=sender)

        # Ikkala querysetni birlashtirish
        messages = sent_messages.union(received_messages).order_by("timestamp")

        # Agar xabarlar bo‘lmasa
        if not messages.exists():
            return Response({"message": "No messages found between these users."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize va javob qaytarish
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class MessageList_beetween_manager_and_workers_View_For_Worker(APIView):
    def get(self, request, sender_id, receiver_id):
        # Foydalanuvchilarni olish
        sender = get_object_or_404(User, id=sender_id)
        receiver = get_object_or_404(User, id=receiver_id)

        # Sender va receiver o‘rtasidagi barcha xabarlarni olish
        sent_messages = Message.objects.filter(sender=sender, receiver=receiver)
        received_messages = Message.objects.filter(sender=receiver, receiver=sender)

        # Ikkala querysetni birlashtirish
        messages = sent_messages.union(received_messages).order_by("timestamp")

        # Agar xabarlar bo‘lmasa
        if not messages.exists():
            return Response({"message": "No messages found between these users."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize va javob qaytarish
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ManagerAdmin_and_manager_MessageListView_for_admin(APIView):
    def get(self, request, sender_id, receiver_id):
        # Jo‘natuvchi va qabul qiluvchini olish
        sender_user = get_object_or_404(User, id=sender_id)
        receiver_user = get_object_or_404(User, id=receiver_id)

        # Xabarlar faqat manager va admin o‘rtasida bo‘lishi kerak
        sender_bio = get_object_or_404(Bio, user=sender_user)
        receiver_bio = Bio.objects.filter(user=receiver_user).first()  # Admin uchun bo‘lishi shart emas

        if sender_bio.position.lower() not in ["manager", "admin"]:
            return Response(
                {"error": "Only managers and admins can have conversations."},
                status=status.HTTP_403_FORBIDDEN
            )

        if receiver_bio and receiver_bio.position.lower() not in ["manager", "admin"]:
            return Response(
                {"error": "Messages can only be exchanged between managers and admins."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Sender va receiver o‘rtasidagi barcha xabarlarni olish
        sent_messages = Message.objects.filter(sender=sender_user, receiver=receiver_user)
        received_messages = Message.objects.filter(sender=receiver_user, receiver=sender_user)

        # Ikkala querysetni birlashtirish va vaqt bo‘yicha tartiblash
        messages = sent_messages.union(received_messages).order_by("timestamp")

        # Agar xabarlar bo‘lmasa
        if not messages.exists():
            return Response({"message": "No messages found between these users."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize va javob qaytarish
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ManagerAdmin_and_manager_MessageListView_for_Manager(APIView):
    def get(self, request, sender_id, receiver_id):
        # Jo‘natuvchi va qabul qiluvchini olish
        sender_user = get_object_or_404(User, id=sender_id)
        receiver_user = get_object_or_404(User, id=receiver_id)

        # Xabarlar faqat manager va admin o‘rtasida bo‘lishi kerak
        sender_bio = get_object_or_404(Bio, user=sender_user)
        receiver_bio = Bio.objects.filter(user=receiver_user).first()  # Admin uchun bo‘lishi shart emas

        if sender_bio.position.lower() not in ["manager", "admin"]:
            return Response(
                {"error": "Only managers and admins can have conversations."},
                status=status.HTTP_403_FORBIDDEN
            )

        if receiver_bio and receiver_bio.position.lower() not in ["manager", "admin"]:
            return Response(
                {"error": "Messages can only be exchanged between managers and admins."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Sender va receiver o‘rtasidagi barcha xabarlarni olish
        sent_messages = Message.objects.filter(sender=sender_user, receiver=receiver_user)
        received_messages = Message.objects.filter(sender=receiver_user, receiver=sender_user)

        # Ikkala querysetni birlashtirish va vaqt bo‘yicha tartiblash
        messages = sent_messages.union(received_messages).order_by("timestamp")

        # Agar xabarlar bo‘lmasa
        if not messages.exists():
            return Response({"message": "No messages found between these users."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize va javob qaytarish
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ManagerSendMessageToWorkersView(APIView):
    def post(self, request, user_id):
        # Menejerning Bio ma'lumotlarini olish
        manager_bio = get_object_or_404(Bio, user_id=user_id)

        # Menejer ekanligini tekshirish
        if manager_bio.position.lower() != "manager":
            return Response(
                {"error": "Only managers are allowed to send messages to workers."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Menejerning bo‘limidagi ishchilarni topish
        workers = Bio.objects.filter(department=manager_bio.department, position="Worker")

        if not workers.exists():
            return Response(
                {"error": "No workers found in the same department."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Xabar mazmunini olish
        content = request.data.get("content")
        if not content:
            return Response(
                {"error": "Message content is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ishchilarga xabar yuborish
        messages = [
            Message(sender=manager_bio.user, receiver=worker.user, content=content)
            for worker in workers
        ]
        Message.objects.bulk_create(messages)  # Yagona so‘rov bilan bir nechta xabar yaratish

        return Response(
            {"message": "Message sent to all workers in the department."},
            status=status.HTTP_201_CREATED
        )

    
class ManagerSendMessageToAdminView(APIView):
    def post(self, request, user_id):
        # Get the manager's Bio
        manager_bio = get_object_or_404(Bio, user_id=user_id)

        # Ensure the sender is a manager
        if manager_bio.position.lower() != "manager":
            return Response(
                {"error": "Only managers are allowed to send messages to the admin."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the admin user (assuming admin has user_id = 1)
        admin_user = get_object_or_404(User, id=1)

        # Get the message content from the request
        content = request.data.get("content")
        if not content:
            return Response(
                {"error": "Message content is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the message
        message = Message.objects.create(
            sender=manager_bio.user,
            receiver=admin_user,
            content=content
        )

        # Serialize the message and return the response
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AdminSendMessageToManagerView(APIView):
    def post(self, request,receiver_id):
        # Admin foydalanuvchisini olish
        admin_user = get_object_or_404(User, id=1)

        # Admin ekanligini tekshirish (Bio modelidagi pozitsiya orqali)
        admin_bio = get_object_or_404(Bio, user=admin_user)
        if admin_bio.position.lower() != "admin":
            return Response(
                {"error": "Only admins are allowed to send messages to managers."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Xabar yuboriladigan menejerni topish
        manager_bio = get_object_or_404(Bio, user_id=receiver_id)

        # Menejer ekanligini tekshirish
        if manager_bio.position.lower() != "manager":
            return Response(
                {"error": "The recipient must be a manager."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Xabar mazmunini olish
        content = request.data.get("content")
        if not content:
            return Response(
                {"error": "Message content is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Xabar yaratish
        message = Message.objects.create(
            sender=admin_user,
            receiver=manager_bio.user,
            content=content
        )

        # Serialize va javob qaytarish
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
