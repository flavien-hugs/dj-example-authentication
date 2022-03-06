# helpers.utilitary.py

import os
import logging
from hashlib import sha256

from django.utils.text import slugify
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


def upload_image_to(instance, filename):
    ext = filename.split(".")[-1]
    if instance.name:
        filename = f"{instance.name}.{ext}".lower()
    else:
        filename = f"{instance.first_name}.{ext}".lower()
    return os.path.join(instance.file_prepend, filename)
