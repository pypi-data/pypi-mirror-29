from django.db import models


class ImageTag(models.Model):
    """
    Tags represent a type of image, which is used to serialize it.
    """
    name = models.SlugField()

    def __str__(self):
        return self.name
