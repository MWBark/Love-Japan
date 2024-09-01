from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Form class for sending contact message.
    """
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'message' )