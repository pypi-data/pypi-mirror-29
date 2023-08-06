from election.models import ElectionDay
from geography.models import Division, DivisionLevel
from rest_framework import generics
from rest_framework.exceptions import APIException

from electionnight.serializers import (SpecialElectionListSerializer,
                                       SpecialElectionSerializer)


class SpecialMixin(object):
    def get_queryset(self):
        """
        Returns a queryset of all states holding a special election on a date.
        """
        try:
            date = ElectionDay.objects.get(date=self.kwargs['date'])
        except Exception:
            raise APIException(
                'No elections on {}.'.format(self.kwargs['date'])
            )
        division_ids = []
        for election in date.elections.all():
            if (
                election.division.level.name == DivisionLevel.STATE or
                election.division.level.name == DivisionLevel.DISTRICT
            ) and election.race.special:
                division_ids.append(election.division.uid)
        return Division.objects.filter(uid__in=division_ids)

    def get_serializer_context(self):
        """Adds ``election_day`` to serializer context."""
        context = super(SpecialMixin, self).get_serializer_context()
        context['election_date'] = self.kwargs['date']
        return context


class SpecialList(SpecialMixin, generics.ListAPIView):
    serializer_class = SpecialElectionListSerializer


class SpecialDetail(SpecialMixin, generics.RetrieveAPIView):
    serializer_class = SpecialElectionSerializer
