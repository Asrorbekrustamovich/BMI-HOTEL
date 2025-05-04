from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Booking, Status, Room

@receiver(post_save, sender=Booking)
def update_room_status(sender, instance, **kwargs):
    """
    Booking modeli saqlangandan so'ng `room.status` yangilanadi.
    """
    if instance.ordered_time is None and instance.finish_time is None:
        instance.room.status = Status.objects.get(id=2)  # Booked
    elif instance.ordered_time is not None and instance.finish_time is not None:
        if instance.finish_time < now():
            instance.room.status = Status.objects.get(id=4)  # Expired
        else:
            instance.room.status = Status.objects.get(id=3)  # Active

    instance.room.save()
