from django import forms
from .models import Profile, ImagePost


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image', 'bio', )


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = ImagePost
        fields = ('title', 'image', 'message' )
