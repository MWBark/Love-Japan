from django.db import models
from cloudinary.models import CloudinaryField


class ContactInfo(models.Model):
    """
    Stores contact page information.
    """
    title = models.CharField(max_length=200, unique=True)
    image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
