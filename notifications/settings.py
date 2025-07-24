''' Django notifications settings file '''
# -*- coding: utf-8 -*-
from django.conf import settings


CONFIG_DEFAULTS = {
    'SOFT_DELETE': False,
    'NUM_TO_FETCH': 10,
    'CACHE_TIMEOUT': 2,
    'NOTIFICATIONS_SERIALIZER': 'notifications.serializers.NotificationSerializer',
    'ACTOR_OBJECT_IN_RESPONSE': False,
    'ACTION_OBJECT_IN_RESPONSE': False,
    'TARGET_OBJECT_IN_RESPONSE': False,
    'SOCKET_EXTRA_KEYS': [],  # _IN_JWT
}


def get_config():
    user_config = getattr(settings, 'NOTIFICATIONS_CONFIG', {})

    if (extra_jwt_keys := user_config.get("SOCKET_EXTRA_KEYS")) and not isinstance(extra_jwt_keys, list):
        raise Exception("SOCKET_EXTRA_KEYS must be a list.")

    config = CONFIG_DEFAULTS.copy()
    config.update(user_config)

    return config
