from rest_framework import serializers

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # actor_url = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = '__all__'

    # def get_object_url(self, object):
    #     """
    #     Get url representing the object.
    #     This will return instance.get_url_for_notifications()
    #     with parameters `notification` and `request`,
    #     if it is defined and get_absolute_url() otherwise
    #     """
    #     if hasattr(instance, 'get_url_for_notifications'):
    #         return instance.get_url_for_notifications(self, request)
    #     elif hasattr(instance, 'get_absolute_url'):
    #         return instance.get_absolute_url()
    #     return None
