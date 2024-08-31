from django import forms
from .models import Profile, ImagePost, ImageComment


class ProfileForm(forms.ModelForm):
    """
    Form class for users update Profile.  
    """
    class Meta:
        model = Profile
        fields = ('image', 'bio', )


class UploadImageForm(forms.ModelForm):
    """
    Form class for users to upload an ImagePost.  
    """
    class Meta:
        model = ImagePost
        fields = ('title', 'image', 'message', 'tags', )


class ImageCommentForm(forms.ModelForm):
    """
    Form class for users to comment on a post.  
    """
    class Meta:
        model = ImageComment
        fields = ('body',)