from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Invate, Subscribe


@receiver(post_save, sender=Invate)
def create_friendship(sender, instance, created, **kwargs):
    if created:
        opposite_request = Invate.objects.filter(
            receiver=instance.sender, sender=instance.receiver).first()
        if opposite_request:
            Subscribe.objects.create(
                user=instance.sender, author=instance.receiver)
            Subscribe.objects.create(
                user=instance.receiver, author=instance.sender)
            opposite_request.delete()
            instance.delete()
