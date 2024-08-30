from django.contrib.auth.models import User
from .models import Notification


def notification_alert(request):

    notifications = []
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)

    return {"notifications": notifications}