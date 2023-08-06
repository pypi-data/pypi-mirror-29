from rest_framework.reverse import reverse

from .state import StateListSerializer, StateSerializer


class SpecialElectionListSerializer(StateListSerializer):
    def get_url(self, obj):
        return reverse(
            'electionnight_api_special-election-detail',
            request=self.context['request'],
            kwargs={
                'pk': obj.pk,
                'date': self.context['election_date']
            })


class SpecialElectionSerializer(StateSerializer):
    pass
