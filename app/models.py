from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_info")
    bio = models.TextField(null=True, blank=True)
    image=models.ImageField(upload_to='images/',null=True,blank=True)
    def __str__(self):
        return f"User Info for {self.user.username}"

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
class Room(models.Model):
    room_number=models.TextField()
    room_type=models.TextField()
    status=models.TextField()
    price=models.IntegerField()

class Customer(models.Model):
    name=models.TextField()
    contact_info=models.TextField()
    customerinfo=models.TextField()
    created_at=models.DateField(auto_now_add=True)

class Booking(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)    
     customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
     room=models.ForeignKey(Room,on_delete=models.CASCADE)

class ActionType(models.TextChoices):
    CREATE = 'CREATE', 'Create'
    UPDATE = 'UPDATE', 'Update'
    DELETE = 'DELETE', 'Delete'

class History(models.Model):
    model_name = models.CharField(max_length=100)  # e.g., 'Booking', 'Room', etc.
    object_id = models.PositiveIntegerField()  # ID of the object being tracked
    action = models.CharField(max_length=10, choices=ActionType.choices)  # CREATE, UPDATE, DELETE
    data = models.JSONField(null=True, blank=True)  # Store the data that was changed
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the action
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Who performed the action

    def __str__(self):
        return f"{self.action} - {self.model_name} {self.object_id} by {self.user.username if self.user else 'System'} at {self.timestamp}"
