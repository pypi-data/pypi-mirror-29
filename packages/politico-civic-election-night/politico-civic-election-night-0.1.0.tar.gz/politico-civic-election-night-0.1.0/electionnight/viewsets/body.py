from election.models import ElectionDay
from electionnight.serializers import BodyListSerializer, BodySerializer
from government.models import Body
from rest_framework import generics
from rest_framework.exceptions import APIException


class BodyMixin(object):
    def get_queryset(self):
        """
        Returns a queryset of all bodies holding an election on a date.
        """
        try:
            date = ElectionDay.objects.get(date=self.kwargs['date'])
        except Exception:
            raise APIException(
                'No elections on {}.'.format(self.kwargs['date'])
            )
        body_ids = []
        for election in date.elections.all():
            body = election.race.office.body
            if body:
                body_ids.append(body.uid)
        return Body.objects.filter(uid__in=body_ids)

    def get_serializer_context(self):
        """Adds ``election_day`` to serializer context."""
        context = super(BodyMixin, self).get_serializer_context()
        context['election_date'] = self.kwargs['date']
        return context


class BodyList(BodyMixin, generics.ListAPIView):
    serializer_class = BodyListSerializer


class BodyDetail(BodyMixin, generics.RetrieveAPIView):
    serializer_class = BodySerializer
