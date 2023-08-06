import uuid

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from entity.fields import CountryField
from uuslug import uuslug

from .organization_classification import OrganizationClassification


class Organization(models.Model):
    """An org.

    Generally follows the Popolo spec:
    http://www.popoloproject.com/specs/organization.html
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    uid = models.CharField(
        max_length=500,
        editable=False,
        blank=True
    )

    slug = models.SlugField(
        blank=True, max_length=100, unique=True, editable=False
    )

    name = models.CharField(max_length=500)

    identifiers = JSONField(null=True, blank=True)

    classification = models.ForeignKey(
        OrganizationClassification,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='organizations')

    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children')

    national_headquarters = CountryField(default="US")

    founding_date = models.DateField(null=True, blank=True)
    dissolution_date = models.DateField(null=True, blank=True)

    summary = models.CharField(
        max_length=500,
        null=True, blank=True, help_text="A one-line biographical summary.")
    description = models.TextField(
        null=True, blank=True, help_text="A longer-form description.")

    links = ArrayField(
        models.URLField(), blank=True, null=True,
        help_text="External web links, comma-separated.")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`person:{slug}`
        """

        self.slug = uuslug(
            self.name,
            instance=self,
            max_length=100,
            separator='-',
            start_no=2
        )
        if not self.uid:
            self.uid = 'organization:{}'.format(self.slug)

        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.uid
