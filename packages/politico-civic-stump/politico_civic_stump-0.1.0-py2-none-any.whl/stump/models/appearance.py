import datetime

from django.db import models
from election.models import Candidate
from entity.fields import CountryField, StateField
from stump.fields import MarkdownField


class Appearance(models.Model):
    """
    An appearance can only happen on a single date and in a single city.
    """
    # Who
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    # What
    appearance_type = models.ForeignKey(
        'AppearanceType', on_delete=models.PROTECT)
    # When
    date = models.DateField(default=datetime.date.today)
    # Where
    city = models.CharField(max_length=250)
    state = StateField(
        null=True, blank=True, help_text="If visit in U.S.")
    country = CountryField(default='US')
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    # Why
    description = MarkdownField(blank=True, null=True)

    @property
    def person(self):
        return self.candidate.person.full_name

    @property
    def location(self):
        if self.state:
            return '{}, {}'.format(
                self.city,
                self.state
            )
        else:
            return '{}, {}'.format(
                self.city,
                self.get_country_display()
            )

    def __str__(self):
        return '{} - {}: {}'.format(
            self.date,
            self.candidate.person.last_name,
            self.location,
        )

    class Meta:
        unique_together = (
            "candidate",
            "date",
            "city",
            "state",
            "country",
            "appearance_type",
        )
        ordering = ['-date']
