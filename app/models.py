from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name=models.TextField(null=False)
    def __str__(self):
        return self.name
    
class Bio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_info")
    image = models.ImageField(upload_to='images/', null=True, blank=True)  # Profile picture
    bio_text = models.TextField(null=True, blank=True)
    phone_number=models.TextField()  # The actual bio content
    position=models.TextField(null=False)
    email=models.EmailField(null=True,blank=True)
    adress=models.TextField(null=True,blank=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # When the bio was created
    updated_at = models.DateTimeField(auto_now=True)  # When the bio was last updated
    joining_date=models.DateField(auto_created=True)
    def __str__(self):
        return f"User Info for {self.user.username}"

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class Status(models.Model):
    name = models.TextField()

    def __str__(self):
        return f"{self.name}-{self.id}"

class Room(models.Model):
    room_number = models.TextField()
    room_type = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    price = models.IntegerField()

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"

class Customer(models.Model):
    name = models.TextField()
    contact_info = models.TextField()
    customerinfo = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Customer {self.name} - {self.contact_info}"

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking for {self.customer.name} - Room {self.room.room_number}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)    
    class Meta:
        db_table = 'message'
