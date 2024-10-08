from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager

STATUS = ((0, "Draft"), (1, "Approved"))


class Profile(models.Model):
    """
    Extends the :model: `auth.user`
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class ImagePost(models.Model):
    """
    Stores a single image post entry related to :model: `auth.User`.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    uploader = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="image_posts"
    )
    image = CloudinaryField('image')
    message = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="image_like", blank=True)
    tags = TaggableManager()

    # Count likes
    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} by {self.uploader}"


class ImageComment(models.Model):
    """
    Stores a single comment entry related to :model: `main.ImagePost`
    and :model: `auth.User`.
    """
    imagepost = models.ForeignKey(
        ImagePost, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )
    body = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name="image_comment_like", blank=True)

    # Count likes
    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"


class Notification(models.Model):
    """
    Stores a single notification related to :model: `auth.User`.
    """
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.message}" sent to {self.user}'
