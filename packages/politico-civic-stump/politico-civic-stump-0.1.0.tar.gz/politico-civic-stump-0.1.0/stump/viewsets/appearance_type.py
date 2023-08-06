from stump.models import AppearanceType
from stump.serializers import AppearanceTypeSerializer

from .base import BaseViewSet


class AppearanceTypeViewSet(BaseViewSet):
    queryset = AppearanceType.objects.all()
    serializer_class = AppearanceTypeSerializer
