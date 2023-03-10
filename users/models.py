from django.db import models
from django.contrib.auth.models import User

def user_profile_path(instance, filename):
    return 'user/{0}/{1}'.format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= user_profile_path, default="profile-picture.webp")
    bio = models.TextField(blank=True)

    def __str__(self):
        return "{} {}".format(self.user, 'Profile')