from django import forms
from django.contrib import admin
from election.models import Candidate


class CandidateChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, candidate):
        return candidate.person.full_name


class AppearanceForm(forms.ModelForm):
    candidate = CandidateChoiceField(
        queryset=Candidate.objects.all()
    )


class AppearanceAdmin(admin.ModelAdmin):
    search_fields = ['candidate__person__full_name']
    list_filter = ('date', 'appearance_type',)
    actions = None
    fieldsets = (
        (None, {
            'fields': ('candidate', 'appearance_type', 'date',)
        }),
        ('Location', {
            'fields': ('city', 'state', 'country'),
        }),
        ('Geocode', {
            'fields': ('lat', 'lon'),
        }),
        ('Context', {
            'fields': ('description',),
        }),
    )
    list_display = ('date', 'location', 'person', 'appearance_type')
    form = AppearanceForm
