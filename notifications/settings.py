''' Django notifications settings file '''
# -*- coding: utf-8 -*-
from django.conf import settings


CONFIG_DEFAULTS = {
    'PAGINATE_BY': 20,
    'USE_JSONFIELD': False,
    'SOFT_DELETE': False,
    'NUM_TO_FETCH': 10,
    'CACHE_TIMEOUT': 2,
    'NOTIFICATIONS_SERIALIZER': 'notifications.serializers.NotificationSerializer',
}


def get_config():
    user_config = getattr(settings, 'NOTIFICATIONS_CONFIG', {})

    config = CONFIG_DEFAULTS.copy()
    config.update(user_config)

    return config
