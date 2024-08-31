from django.contrib.auth.models import User
from .models import Notification


def notification_alert(request):

    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_on')

    return {"unread_notifications": unread_notifications}