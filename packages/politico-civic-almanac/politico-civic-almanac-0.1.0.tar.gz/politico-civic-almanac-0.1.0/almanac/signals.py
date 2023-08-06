from django.db.models.signals import post_save
from django.dispatch import receiver

from .celery import serialize_calendar
from .models import ElectionEvent


@receiver(post_save, sender=ElectionEvent)
def election_event_save(sender, instance, **kwargs):
    serialize_calendar.delay(
        instance.election_day.cycle.name,
        instance.division,
        instance.has_senate_election(),
        instance.has_house_election()
    )
