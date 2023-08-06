from rest_framework import serializers
from stump.models import AppearanceType


class AppearanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppearanceType
        fields = '__all__'
