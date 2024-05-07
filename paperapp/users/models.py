from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    """
    User Profile Model (one-to-one relationship with User model).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self):
        return self.user.username

    def save(
        self, *args, **kwargs
    ):
        """
        Crop the input image to a square and save it.
        """
        super().save(*args, **kwargs)
        if self.avatar:
            image = Image.open(self.avatar)
            width, height = image.size
            if width != height:
                crop = min(width, height)
                left = (width - crop) / 2
                top = (height - crop) / 2
                right = (width + crop) / 2
                bottom = (height + crop) / 2
                image = image.crop((left, top, right, bottom))
                image.save(self.avatar.path)
