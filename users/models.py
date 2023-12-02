from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profile_avatars", default="avatar.jpg")
    about = models.CharField(max_length=1000, null=True, blank=True)
    twitter_bio = models.URLField(null=True, blank=True)
    youtube_bio = models.URLField(null=True, blank=True)
    facebook_bio = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    # resize profile avatar before saving to the database
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        # resize image
        output_size = (300, 300)
        # create a thumbnail
        img.thumbnail(output_size)
        # overwrite old image
        img.save(self.avatar.path)
