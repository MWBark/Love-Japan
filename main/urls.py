from . import views
from django.urls import path

urlpatterns = [
    path('', views.ImagePostList.as_view(), name='home'),
    path('imagepost/<slug:slug>/', views.imagepost, name='imagepost'),
    path('imagepost/<slug:slug>/edit_comment/<int:comment_id>',
        views.comment_edit, name='comment_edit'),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('profile/<int:pk>/imageposts', views.ProfilePostList.as_view(), name="profile-posts"),
    path('uploadimage', views.upload_image, name="upload-image"),
]