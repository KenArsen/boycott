import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.product.models import Product


@receiver(post_delete, sender=Product)
def delete_profile_files(sender, instance, **kwargs):
    """
    Deletes avatar and QR code files when a profile is deleted.
    """
    if instance.image and os.path.isfile(instance.image.path):
        print("#" * 20)
        print(instance.image.path)
        print("#" * 20)
        os.remove(instance.image.path)
