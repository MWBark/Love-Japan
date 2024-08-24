from django import forms
from .models import Profile, ImagePost, ImageComment


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image', 'bio', )


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = ImagePost
        fields = ('title', 'image', 'message' )


class ImageCommentForm(forms.ModelForm):
    """
    Form class for users to comment on a post.  
    """
    class Meta:
        model = ImageComment
        fields = ('body',)