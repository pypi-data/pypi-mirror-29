from django.contrib import admin

from stump.models import Appearance, AppearanceType
from .appearance import AppearanceAdmin

admin.site.register(AppearanceType)
admin.site.register(Appearance, AppearanceAdmin)
