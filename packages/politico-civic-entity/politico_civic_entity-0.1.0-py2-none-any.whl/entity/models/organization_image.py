import os
import uuid

from django.db import models
from django.utils.html import format_html
from entity.utils.aws import StorageService

from .image_tag import ImageTag
from .organization import Organization


def person_image_path(instance, filename):
    return os.path.join(
        'cdn/images/organizations',
        instance.person.slug,
        '{}-{}{}'.format(
            instance.tag,
            uuid.uuid4().hex[:6],
            os.path.splitext(filename)[1]
        )
    )


class OrganizationImage(models.Model):
    """
    Image attached to a person, which can be serialized
    by a tag.
    """
    organization = models.ForeignKey(
        Organization, related_name='images', on_delete=models.PROTECT)
    tag = models.ForeignKey(
        ImageTag, related_name="+",
        on_delete=models.PROTECT,
        help_text="Used to serialize images.")
    image = models.ImageField(
        upload_to=person_image_path,
        storage=StorageService()
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def preview(self):
        return format_html(
            '<a href="{0}" target="_blank">'
            '<img src="{0}" style="max-height:100px; max-width: 300px;">'
            '</a>'.format(self.image.url)
        )

    class Meta:
        unique_together = ('organization', 'tag')

    def __str__(self):
        return '{} {}'.format(self.organization.slug, self.tag.name)
