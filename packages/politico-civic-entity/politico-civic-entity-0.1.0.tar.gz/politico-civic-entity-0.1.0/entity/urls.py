from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import (ImageTagViewSet, OrganizationClassificationViewSet,
                       OrganizationViewSet, PersonViewSet)

router = DefaultRouter()
router.register(r'people', PersonViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'image-tags', ImageTagViewSet)
router.register(
    r'organization-classifications',
    OrganizationClassificationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
