from django.db.models.signals import post_save
from django.dispatch import receiver
from geopy.geocoders import GoogleV3
from stump.conf import settings
from stump.models import Appearance


@receiver(post_save, sender=Appearance)
def geocode(sender, instance, created, **kwargs):
    # TODO Move this into a celery task.
    if not instance.lat or not instance.lon:
        geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_GEOCODING_API_KEY)
        state = instance.get_state_display() if instance.state else None
        location = geolocator.geocode(
            '{}, {} {}'.format(
                instance.city,
                state,
                instance.get_country_display()
            )
        )
        instance.lat = location.latitude
        instance.lon = location.longitude
        instance.save()
