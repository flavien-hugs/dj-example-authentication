# account.models.py


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from helpers.utilitary import upload_image_to

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust


NULL_AND_BLANK = {'null': True, 'blank': True}


class User(AbstractUser):

    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    file_prepend = "upload/user/profile/"

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné(e)')
    )

    email = models.EmailField(
        verbose_name='adresse email',
        max_length=80, unique=True,
        help_text="Enter user adresse email."
    )
    role = models.CharField(
        max_length=30,
        default=SUBSCRIBER,
        choices=ROLE_CHOICES,
        verbose_name="Rôle",
        help_text="Choice the user role."
    )
    picture = models.ImageField(
        upload_to=upload_image_to,
        verbose_name="Photo de profile",
        validators=[
            FileExtensionValidator(['jpeg', 'jpg', 'png'])
        ],
        help_text="Add user profile image",
        **NULL_AND_BLANK
    )
    formatted_image = ImageSpecField(
        source='picture',
        processors=[
            Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(120, 120)
        ],
        format='JPEG',
        options={'quality': 90}
    )

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural = 'utilisateurs'
        indexes = [models.Index(fields=['id'])]


    def __str__(self):
        return self.first_name

    def get_profile_image(self):
        if self.formatted_image:
            return self.formatted_image.url
        return 'https://via.placeholder.com/300'
