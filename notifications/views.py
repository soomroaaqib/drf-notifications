from django.utils.module_loading import import_string
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from swapper import load_model

from notifications import settings as notification_settings

Notification = load_model('notifications', 'Notification')

class NotificationViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    serializer_class = None
    _serializer_class = notification_settings.get_config()["NOTIFICATIONS_SERIALIZER"]

    def get_serializer_class(self):
        """
        If serializer_class is set, use it directly. Otherwise get the class from settings.
        """

        if self.serializer_class:
            return self.serializer_class
        try:
            return import_string(self._serializer_class)
        except ImportError:
            msg = "Could not import serializer '%s'" % self._serializer_class
            raise ImportError(msg)

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)

        if self.action in ("list", "count"):
            if notification_settings.get_config()['SOFT_DELETE']:
                queryset = queryset.active()
        elif self.action in ("unread", "unread_count", "mark_as_read", "mark_all_as_read"):
            queryset = queryset.unread()
        elif self.action in ("read", "read_count", "mark_as_unread"):
            queryset = queryset.read()

        return queryset
    
    @action(["get"], detail=False)
    def read(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(["get"], detail=False)
    def unread(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(["get"], detail=False)
    def read_count(self, request, *args, **kwargs):
        data = {'count': request.user.notifications.read().count()}
        return Response(data)

    @action(["get"], detail=False)
    def unread_count(self, request, *args, **kwargs):
        data = {'count': request.user.notifications.unread().count()}
        return Response(data)

    @action(["get"], detail=False)
    def count(self, request, *args, **kwargs):
        data = {'count': request.user.notifications.count()}
        return Response(data)

    @action(["put"], detail=True)
    def mark_as_read(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.mark_as_read()
        return super().list(request, *args, **kwargs)

    @action(["put"], detail=True)
    def mark_as_unread(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.mark_as_unread()
        return super().list(request, *args, **kwargs)

    @action(["put"], detail=False)
    def mark_all_as_read(self, request, *args, **kwargs):
        request.user.notifications.mark_all_as_read()
        return super().list(request, *args, **kwargs)
