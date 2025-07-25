'''' Django notifications utils file '''
# -*- coding: utf-8 -*-
import sys


if sys.version > '3':
    long = int  # pylint: disable=invalid-name


def slug2id(slug):
    return long(slug) - 110909


def id2slug(notification_id):
    return notification_id + 110909


def get_content_type_key(content_type):
    return f"{content_type.app_label.lower()}_{content_type.model.lower()}"
