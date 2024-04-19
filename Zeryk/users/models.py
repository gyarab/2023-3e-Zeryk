from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(
        upload_to='pfp',
        null=True,
        blank=True,
        default='pfp/default.png'
    )

    def __str__(self):
        return self.user.username

@receiver(pre_save, sender=User)
def handle(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()