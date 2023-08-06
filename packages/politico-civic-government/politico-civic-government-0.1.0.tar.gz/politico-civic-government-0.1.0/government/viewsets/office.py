from government.models import Office
from government.serializers import OfficeSerializer

from .base import BaseViewSet


class OfficeViewSet(BaseViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
