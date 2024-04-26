from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from recipes.models import Recipe

#tento model slouží k uchování dalších informací o uživateli, které nejsou součástí základního modelu User. Profil uživatele.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(
        upload_to='pfp',
        null=True,
        blank=True,
        default='pfp/default.png',
        verbose_name=_('pfp'),
    )
    liked_recipes = models.ManyToManyField(Recipe)

    #metoda, která vrací výchozí profilový obrázek. 
    def get_default_pfp(self):
        return 'pfp/default.png'
    
    #metoda, která definuje textovou reprezentaci instance UserProfile.
    def __str__(self):
        return self.user.username

#definuje signál, který reaguje na událost post_save (po uložení) pro model User. Když se instance modelu User uloží, tento signál se aktivuje.
@receiver(post_save, sender=User)
def handle(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()