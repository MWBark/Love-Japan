from . import views
from django.urls import path

urlpatterns = [
    path('', views.ImagePostList.as_view(), name='home'),
    path('imagepost/<slug:slug>/', views.imagepost, name='imagepost'),
    path('imagepost/<slug:slug>/edit_comment/<int:comment_id>',
        views.comment_edit, name='comment_edit'),
    path('imagepost/<slug:slug>/delete_comment/<int:comment_id>',
        views.comment_delete, name='comment_delete'),
    path('imagepost/<slug:slug>/like_comment/<int:comment_id>',
        views.comment_like, name='comment_like'),
    path('imagepost/<slug:slug>/edit_post', views.imagepost_edit, name='imagepost_edit'),
    path('imagepost/<slug:slug>/delete_post', views.imagepost_delete, name='imagepost_delete'),
    path('imagepost/<slug:slug>/imagepost_like', views.imagepost_like, name='imagepost_like'),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('profile/<int:pk>/imageposts', views.ProfilePostList.as_view(), name="profile-posts"),
    path('uploadimage', views.upload_image, name="upload-image"),
]