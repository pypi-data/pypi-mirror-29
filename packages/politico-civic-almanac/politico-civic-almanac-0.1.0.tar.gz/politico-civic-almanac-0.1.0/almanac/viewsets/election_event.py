from almanac.models import ElectionEvent
from almanac.serializers import ElectionEventSerializer

from .base import BaseViewSet


class ElectionEventViewSet(BaseViewSet):
    serializer_class = ElectionEventSerializer

    def get_queryset(self):
        queryset = ElectionEvent.objects.all().order_by(
            'election_day__date', 'division__label'
        )

        state = self.request.query_params.get('state', None)
        if state is not None:
            queryset = queryset.filter(division__slug=state)
        else:
            queryset = queryset.exclude(event_type=ElectionEvent.GENERAL)

        body = self.request.query_params.get('body', None)
        if body is not None:
            queryset = queryset.exclude(event_type=ElectionEvent.GENERAL)
            if body == 'senate':
                queryset = [q for q in queryset if q.has_senate_election()]
            elif body == 'house':
                queryset = [q for q in queryset if q.has_house_election()]

        else:
            queryset = queryset.exclude(event_type=ElectionEvent.GENERAL)

        return queryset
