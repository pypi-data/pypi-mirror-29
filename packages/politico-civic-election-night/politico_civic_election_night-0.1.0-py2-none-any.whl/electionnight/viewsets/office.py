from election.models import ElectionDay
from electionnight.serializers import OfficeListSerializer, OfficeSerializer
from government.models import Office
from rest_framework import generics
from rest_framework.exceptions import APIException


class OfficeMixin(object):
    def get_queryset(self):
        """
        Returns a queryset of all executive offices holding an election on
        a date.
        """
        try:
            date = ElectionDay.objects.get(date=self.kwargs['date'])
        except Exception:
            raise APIException(
                'No elections on {}.'.format(self.kwargs['date'])
            )
        office_ids = []
        for election in date.elections.all():
            office = election.race.office
            if not office.body:
                office_ids.append(office.uid)
        return Office.objects.filter(uid__in=office_ids)

    def get_serializer_context(self):
        """Adds ``election_day`` to serializer context."""
        context = super(OfficeMixin, self).get_serializer_context()
        context['election_date'] = self.kwargs['date']
        return context


class OfficeList(OfficeMixin, generics.ListAPIView):
    serializer_class = OfficeListSerializer


class OfficeDetail(OfficeMixin, generics.RetrieveAPIView):
    serializer_class = OfficeSerializer
