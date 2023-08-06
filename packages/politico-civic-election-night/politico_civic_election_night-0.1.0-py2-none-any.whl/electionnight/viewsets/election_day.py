from election.models import ElectionDay
from electionnight.serializers import ElectionDaySerializer
from rest_framework import generics


class ElectionDayList(generics.ListAPIView):
    serializer_class = ElectionDaySerializer
    queryset = ElectionDay.objects.all()


class ElectionDayDetail(generics.RetrieveAPIView):
    serializer_class = ElectionDaySerializer
    queryset = ElectionDay.objects.all()
