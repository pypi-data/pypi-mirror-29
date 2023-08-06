from stump.models import Appearance
from stump.serializers import AppearanceSerializer

from .base import BaseViewSet


class AppearanceViewSet(BaseViewSet):
    queryset = Appearance.objects.all()
    serializer_class = AppearanceSerializer
