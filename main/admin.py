from django.contrib import admin
from .models import Profile, ImagePost, ImageComment, Notification

# Register your models here.
admin.site.register(Profile)

@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(ImageComment)
admin.site.register(Notification)