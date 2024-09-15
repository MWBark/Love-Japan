from django.contrib.auth.models import User
from .models import Notification


def notification_alert(request):
    """
    Filters :model:`main.Notification`.
    by request.user and is_read=False
    orders by newest first

    **Context**

    ``unread_notifications``
        current registerd user notifications where is_read=False.
    """

    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            user=request.user, is_read=False).order_by('-created_on')

    return {"unread_notifications": unread_notifications}
