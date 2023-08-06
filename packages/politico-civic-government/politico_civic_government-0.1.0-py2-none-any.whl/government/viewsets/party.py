from government.models import Party
from government.serializers import PartySerializer

from .base import BaseViewSet


class PartyViewSet(BaseViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
