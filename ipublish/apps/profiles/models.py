from django.db import models
from ipublish.apps.core.models import AbstractTimeStampedModel

class Profile(AbstractTimeStampedModel):

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)

    bio = models.TextField(blank=True)

    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username