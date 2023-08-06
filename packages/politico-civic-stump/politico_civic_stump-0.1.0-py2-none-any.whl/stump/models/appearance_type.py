from django.db import models
from uuslug import uuslug


class AppearanceType(models.Model):
    """
    A type of political appearance.
    """
    slug = models.SlugField(
        blank=True, max_length=100, unique=True, editable=False
    )
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`person:{slug}`
        """
        self.slug = uuslug(
            self.name,
            instance=self,
            max_length=100,
            separator='-',
            start_no=2
        )
        super(AppearanceType, self).save(*args, **kwargs)
