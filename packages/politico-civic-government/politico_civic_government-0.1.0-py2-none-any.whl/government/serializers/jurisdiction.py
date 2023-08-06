from government.models import Jurisdiction
from rest_framework import serializers


class JurisdictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jurisdiction
        fields = '__all__'
