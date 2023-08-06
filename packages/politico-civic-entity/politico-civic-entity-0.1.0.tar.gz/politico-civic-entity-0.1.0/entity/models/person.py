import uuid

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from entity.fields import CountryField, GenderField, RaceField, StateField
from uuslug import uuslug


class Person(models.Model):
    """A real human being.🎵

    Generally follows the Popolo spec:
    http://www.popoloproject.com/specs/person.html
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
        blank=True, max_length=255, unique=True, editable=False
    )

    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=10, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)

    identifiers = JSONField(null=True, blank=True)

    gender = GenderField(null=True, blank=True)
    race = RaceField(null=True, blank=True)
    nationality = CountryField(default='US')

    state_of_residence = StateField(
        null=True, blank=True, help_text="If U.S. resident.")

    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

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
        if not self.full_name:
            self.full_name = '{0}{1}{2}'.format(
                self.first_name,
                '{}'.format(
                    ' ' + self.middle_name + ' ' if self.middle_name else ' ',
                ),
                self.last_name,
                '{}'.format(' ' + self.suffix if self.suffix else '')
            )

        self.slug = uuslug(
            self.full_name,
            instance=self,
            max_length=100,
            separator='-',
            start_no=2
        )
        if not self.uid:
            self.uid = 'person:{}'.format(self.slug)

        super(Person, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "People"

    def __str__(self):
        return self.full_name
