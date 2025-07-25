import swapper
from django.contrib import admin
from notifications.admin import AbstractNotificationAdmin

Notification = swapper.load_model('notifications', 'Notification')


@admin.register(Notification)
class NotificationAdmin(AbstractNotificationAdmin):
    pass
