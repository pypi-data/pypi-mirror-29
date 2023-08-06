from election.models import ElectionDay
from rest_framework import serializers
from rest_framework.reverse import reverse


class ElectionDaySerializer(serializers.ModelSerializer):
    states = serializers.SerializerMethodField()
    bodies = serializers.SerializerMethodField()
    executive_offices = serializers.SerializerMethodField()
    special_elections = serializers.SerializerMethodField()

    def get_states(self, obj):
        """States holding a non-special election on election day."""
        return reverse(
            'electionnight_api_state-election-list',
            request=self.context['request'],
            kwargs={'date': obj.date}
        )

    def get_bodies(self, obj):
        """Bodies with offices up for election on election day."""
        return reverse(
            'electionnight_api_body-election-list',
            request=self.context['request'],
            kwargs={'date': obj.date}
        )

    def get_executive_offices(self, obj):
        """Executive offices up for election on election day."""
        return reverse(
            'electionnight_api_office-election-list',
            request=self.context['request'],
            kwargs={'date': obj.date}
        )

    def get_special_elections(self, obj):
        """States holding a special election on election day."""
        return reverse(
            'electionnight_api_special-election-list',
            request=self.context['request'],
            kwargs={'date': obj.date}
        )

    class Meta:
        model = ElectionDay
        fields = (
            'date',
            'cycle',
            'states',
            'bodies',
            'executive_offices',
            'special_elections',
        )
