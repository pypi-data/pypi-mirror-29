from django.urls import include, path
from rest_framework import routers

from .viewsets import (BodyViewSet, JurisdictionViewSet, OfficeViewSet,
                       PartyViewSet)

router = routers.DefaultRouter()

router.register(r'bodies', BodyViewSet)
router.register(r'jurisdictions', JurisdictionViewSet)
router.register(r'offices', OfficeViewSet)
router.register(r'parties', PartyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
