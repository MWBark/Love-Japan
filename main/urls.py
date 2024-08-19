from . import views
from django.urls import path

urlpatterns = [
    path('', views.ImagePostList.as_view(), name='home'),
    path('<slug:slug>', views.imagepost, name='imagepost'),
]