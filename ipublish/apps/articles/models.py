from django.db import models
from ipublish.apps.core.models import AbstractTimeStampedModel

class Article(AbstractTimeStampedModel):

    slug = models.SlugField(db_index=True, max_length=255, unique=True)

    title = models.CharField(db_index=True, max_length=50)

    description = models.TextField()

    body = models.TextField()

    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='articles')


    def __str__(self):
        return self.title