from rest_framework import serializers
from .models import Role, Bio, UserRole, Room, Customer, Booking, Status,Message,Department,Roomtype
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Bio, Role
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework import serializers
from django.contrib.auth.models import User
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roomtype
        fields='__all__'
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bio
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=False,   # Password is not required for updates
        allow_blank=True  # Allow blank passwords (optional)
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # Store the password in plain text (not recommended)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update the password in plain text (not recommended)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        # Include the password in the response for GET requests
        representation = super().to_representation(instance)
        representation['password'] = instance.password  # Plain text password
        return representation 


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data