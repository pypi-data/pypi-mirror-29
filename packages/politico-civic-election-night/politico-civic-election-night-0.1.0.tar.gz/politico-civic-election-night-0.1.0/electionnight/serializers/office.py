from election.models import Election, ElectionDay
from geography.models import Division
from government.models import Office, Party
from rest_framework import serializers
from rest_framework.reverse import reverse

from electionnight.models import PageContent

from .division import DivisionSerializer
from .election import ElectionSerializer
from .party import PartySerializer


class OfficeListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse(
            'electionnight_api_office-election-detail',
            request=self.context['request'],
            kwargs={
                'pk': obj.pk,
                'date': self.context['election_date']
            })

    class Meta:
        model = Division
        fields = (
            'url',
            'uid',
            'name',
        )


class OfficeSerializer(serializers.ModelSerializer):
    division = serializers.SerializerMethodField()
    parties = serializers.SerializerMethodField()
    elections = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_division(self, obj):
        """Division."""
        return DivisionSerializer(obj.division).data

    def get_parties(self, obj):
        """All parties."""
        return PartySerializer(Party.objects.all(), many=True).data

    def get_elections(self, obj):
        """All elections on an election day."""
        election_day = ElectionDay.objects.get(
            date=self.context['election_date'])
        elections = Election.objects.filter(
            race__office=obj,
            election_day=election_day
        )
        return ElectionSerializer(elections, many=True).data

    def get_content(self, obj):
        """All content for office's page on an election day."""
        election_day = ElectionDay.objects.get(
            date=self.context['election_date'])
        return PageContent.objects.office_content(election_day, obj)

    class Meta:
        model = Office
        fields = (
            'uid',
            'content',
            'elections',
            'parties',
            'division',
        )
