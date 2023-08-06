from django.urls import include, path
from rest_framework import routers

from .viewsets import AppearanceTypeViewSet, AppearanceViewSet

router = routers.DefaultRouter()

router.register(r'appearances', AppearanceViewSet)
router.register(r'appearance-types', AppearanceTypeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
