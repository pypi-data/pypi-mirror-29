from django.contrib import admin
from entity.models import (ImageTag, Organization, OrganizationClassification,
                           OrganizationImage, Person, PersonImage)
from .person import PersonAdmin
from .organization import OrganizationAdmin

admin.site.register(ImageTag)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationImage)
admin.site.register(OrganizationClassification)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonImage)
