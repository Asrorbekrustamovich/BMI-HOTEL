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
        required=False,
        allow_blank=True,
        write_only=True
    )
    role = serializers.CharField(write_only=True, required=False)  # Accept role in input
    role_name = serializers.SerializerMethodField(read_only=True)   # Show role in output

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role', 'role_name']

    def get_role_name(self, obj):
        user_role = UserRole.objects.filter(user=obj).first()
        return user_role.role.name if user_role else None

    def create(self, validated_data):
        role_name = validated_data.pop('role', None)
        user = User(**validated_data)
        if validated_data.get("password"):
            user.set_password(validated_data["password"])
        user.save()

        if role_name:
            role_obj = Role.objects.filter(name=role_name).first()
            if role_obj:
                UserRole.objects.create(user=user, role=role_obj)

        return user

    def update(self, instance, validated_data):
        role_name = validated_data.pop('role', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        if role_name:
            role_obj = Role.objects.filter(name=role_name).first()
            if role_obj:
                user_role, created = UserRole.objects.get_or_create(user=instance)
                user_role.role = role_obj
                user_role.save()

        return instance


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