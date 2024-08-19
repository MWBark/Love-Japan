from . import views
from django.urls import path

urlpatterns = [
    path('', views.ImagePostList.as_view(), name='home'),
    path('imagepost/<slug:slug>', views.imagepost, name='imagepost'),
    path('profile/<int:pk>', views.profile, name="profile"),

]