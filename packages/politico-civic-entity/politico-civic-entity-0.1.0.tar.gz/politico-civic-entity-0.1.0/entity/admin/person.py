from django.contrib import admin
from entity.models import PersonImage


class PersonImageInline(admin.StackedInline):
    model = PersonImage
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    inlines = [
        PersonImageInline,
    ]

    fieldsets = (
        ('Name', {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'suffix',
                'full_name'
            )
        }),
        ('Demogaphics', {
            'fields': ('gender', 'race', 'nationality', 'state_of_residence',),
        }),
        (None, {
            'fields': ('birth_date', 'death_date',),
        }),
        ('Descriptions', {
            'fields': ('summary', 'description', 'identifiers', 'links'),
        }),
        ('Record locators', {
            'fields': ('id', 'uid', 'slug',),
        }),
    )
    readonly_fields = (
        'id',
        'uid',
        'slug',
    )
