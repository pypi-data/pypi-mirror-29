from rest_framework import serializers
from stump.models import Appearance


class AppearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appearance
        fields = '__all__'
