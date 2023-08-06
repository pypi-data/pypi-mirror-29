from django.db import models
from election.models import ElectionDay, Election
from geography.models import Division
from government.models import Body
from uuslug import uuslug

from almanac.fields import MarkdownField


class ElectionEvent(models.Model):
    """A statewide election event"""
    PRIMARIES = 'Primaries'
    PRIMARIES_RUNOFF = 'Primaries Runoff'
    GENERAL = 'General'
    GENERAL_RUNOFF = 'General Runoff'
    SPECIAL_PRIMARY = 'Special Primary'
    SPECIAL_RUNOFF = 'Special Runoff'
    SPECIAL_GENERAL = 'Special General'

    EVENT_TYPES = (
        (PRIMARIES, 'Primaries'),
        (PRIMARIES_RUNOFF, 'Primaries Runoff'),
        (GENERAL, 'General'),
        (GENERAL_RUNOFF, 'General Runoff'),
        (SPECIAL_PRIMARY, 'Special Primary'),
        (SPECIAL_RUNOFF, 'Special Runoff'),
        (SPECIAL_GENERAL, 'Special General')
    )

    OPEN = 'open'
    SEMI_OPEN = 'semi-open'
    SEMI_CLOSED = 'semi-closed'
    CLOSED = 'closed'
    JUNGLE = 'jungle'

    PRIMARY_TYPES = (
        (OPEN, 'Open'),
        (SEMI_OPEN, 'Semi-open'),
        (SEMI_CLOSED, 'Semi-closed'),
        (CLOSED, 'Closed'),
        (JUNGLE, 'Jungle')
    )

    slug = models.SlugField(
        blank=True, max_length=255, unique=True, editable=False)
    label = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    dem_primary_type = models.CharField(
        max_length=50,
        choices=PRIMARY_TYPES,
        null=True, blank=True
    )
    gop_primary_type = models.CharField(
        max_length=50,
        choices=PRIMARY_TYPES,
        null=True, blank=True
    )
    description = MarkdownField(null=True, blank=True)
    election_day = models.ForeignKey(ElectionDay, on_delete=models.PROTECT)
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    early_vote_start = models.DateField(null=True, blank=True)
    early_vote_close = models.DateField(null=True, blank=True)
    vote_by_mail_application_deadline = models.DateField(null=True, blank=True)
    vote_by_mail_ballot_deadline = models.DateField(null=True, blank=True)
    online_registration_deadline = models.DateField(null=True, blank=True)
    registration_deadline = models.DateField(null=True, blank=True)
    poll_closing_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = '{0}-{1}'.format(self.label, self.election_day.cycle.name)

            self.slug = uuslug(
                slug,
                instance=self,
                max_length=100,
                separator='-',
                start_no=2
            )

        super(ElectionEvent, self).save(*args, **kwargs)

    def get_statewide_offices(self):
        statewide_elections = Election.objects.filter(
            election_day=self.election_day,
            division=self.division
        )

        offices = []
        for election in statewide_elections:
            offices.append(election.race.office)

        return set(offices)

    def get_district_offices(self):
        district_elections = Election.objects.filter(
            election_day=self.election_day,
            division__parent=self.division
        )

        offices = []
        for election in district_elections:
            offices.append(election.race.office)

        return set(offices)

    def has_senate_election(self):
        offices = self.get_statewide_offices()
        senate = Body.objects.get(
            label='U.S. Senate'
        )

        for office in offices:
            if office.body == senate:
                return True

        return False

    def has_house_election(self):
        offices = self.get_district_offices()
        house = Body.objects.get(
            label='U.S. House of Representatives'
        )

        for office in offices:
            if office.body == house:
                return True

        return False

    def has_governor_election(self):
        offices = self.get_statewide_offices()
        for office in offices:
            if office.slug.endswith('governor'):
                return True

        return False
