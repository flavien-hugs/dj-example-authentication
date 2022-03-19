# helpers.utilitary.py

import os
import six
import logging
import threading
from hashlib import sha256

from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator

logger = logging.getLogger(__name__)


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def upload_image_to(instance, filename):
    ext = filename.split(".")[-1]
    if instance.name:
        filename = f"{instance.name}.{ext}".lower()
    else:
        filename = f"{instance.first_name}.{ext}".lower()
    return os.path.join(instance.file_prepend, filename)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, date_joined):
        return (
            six.text_type(user.pk)
            + six.text_type(date_joined)
            + six.text_type(user.is_active)
        )


generate_token = TokenGenerator()
