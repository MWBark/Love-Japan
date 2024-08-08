from django.contrib import admin
from .models import Profile, ImagePost

# Register your models here.
admin.site.register(Profile)

@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}