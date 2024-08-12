from django.shortcuts import render
from django.views import generic
from .models import ImagePost


# Create your views here.
class ImagePostList(generic.ListView):
    queryset = ImagePost.objects.all()
    template_name = "main/index.html"