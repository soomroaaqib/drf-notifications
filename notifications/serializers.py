from rest_framework import serializers

from .models import Notification
from .utils import get_content_type_key


class NotificationSerializer(serializers.ModelSerializer):
    action_object_key = serializers.SerializerMethodField()
    target_key = serializers.SerializerMethodField()
    actor_key = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = '__all__'

    def get_action_object_key(self, obj):
        if content_type := obj.action_object_content_type:
            return get_content_type_key(content_type)
        return None

    def get_target_key(self, obj):
        if content_type := obj.target_content_type:
            return get_content_type_key(content_type)
        return None

    def get_actor_key(self, obj):
        if content_type := obj.actor_content_type:
            return get_content_type_key(content_type)
        return None

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
