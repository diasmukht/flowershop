import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from FlowersShop import settings


class Profile(models.Model):
    USER_STATUS = [
        ('regular', 'Обычный'),
        ('advanced', 'Продвинутый'),
        ('vip', 'VIP'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    status = models.CharField(
        max_length=10,
        choices=USER_STATUS,
        default='regular'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default=''
    )
    address = models.TextField(
        blank=True,
        default=''
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        default='default.png'
    )

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url') and self.avatar.name != 'default.png':
            return self.avatar.url
        return settings.MEDIA_URL + 'avatars/default.png'

    def __str__(self):
        return f"Профиль {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

