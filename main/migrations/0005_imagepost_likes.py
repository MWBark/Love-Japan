# Generated by Django 4.2.14 on 2024-08-28 11:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_imagecomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagepost',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='image_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
