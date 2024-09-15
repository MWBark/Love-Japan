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


class ContactMessage(models.Model):
    """
    Stores a single contact message.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    username = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact message from {self.name}"
