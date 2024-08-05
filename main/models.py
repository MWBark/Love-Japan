from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    """
    Extends the :model: `auth.user`
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)