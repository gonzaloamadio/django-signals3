from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from . import models as entities_models

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_create_profile(sender, instance, created, **kwargs):
    """
        Depending of user_type on the User model, we want to create
        a specific "type of profile"
    """
    if created:
        # Here we will put the logic of which type of user we will create.
        # Will be dicted by the type of user, given by the user_type field.
        if instance.user_type == 1:
            entities_models.Person.objects.create(user=instance)
        elif instance.user_type == 2:
            entities_models.Company.objects.create(user=instance)
        else:
            pass
