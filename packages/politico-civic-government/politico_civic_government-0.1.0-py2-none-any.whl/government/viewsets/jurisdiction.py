from government.models import Jurisdiction
from government.serializers import JurisdictionSerializer

from .base import BaseViewSet


class JurisdictionViewSet(BaseViewSet):
    queryset = Jurisdiction.objects.all()
    serializer_class = JurisdictionSerializer
