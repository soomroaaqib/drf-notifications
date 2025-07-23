from rest_framework import serializers
from swapper import load_model

from .settings import get_config
from .utils import get_content_type_key

Notification = load_model('notifications', 'Notification')


def serialize_object(_object):
    class ObjectSerializer(serializers.ModelSerializer):
        class Meta:
            model = _object.__class__
            fields = '__all__'

    return ObjectSerializer(_object).data


class NotificationSerializer(serializers.ModelSerializer):
    action_object_key = serializers.SerializerMethodField()
    target_key = serializers.SerializerMethodField()
    actor_key = serializers.SerializerMethodField()

    if get_config()["ACTOR_OBJECT_IN_RESPONSE"]:
        actor = serializers.SerializerMethodField()

    if get_config()["ACTION_OBJECT_IN_RESPONSE"]:
        action_object = serializers.SerializerMethodField()

    if get_config()["TARGET_OBJECT_IN_RESPONSE"]:
        target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = '__all__'

    def get_action_object(self, obj):
        if obj.action_object:
            return serialize_object(obj.action_object)
        return None

    def get_action_object_key(self, obj):
        if content_type := obj.action_object_content_type:
            return get_content_type_key(content_type)
        return None

    def get_target(self, obj):
        if obj.target:
            return serialize_object(obj.target)
        return None

    def get_target_key(self, obj):
        if content_type := obj.target_content_type:
            return get_content_type_key(content_type)
        return None

    def get_actor(self, obj):
        if obj.actor:
            return serialize_object(obj.actor)
        return None

    def get_actor_key(self, obj):
        if content_type := obj.actor_content_type:
            return get_content_type_key(content_type)
        return None
