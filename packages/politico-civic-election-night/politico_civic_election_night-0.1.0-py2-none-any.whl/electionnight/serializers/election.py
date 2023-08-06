import us
from election.models import Candidate, CandidateElection, Election
from entity.models import Person
from geography.models import Division, DivisionLevel
from government.models import Office
from rest_framework import serializers

from electionnight.models import APElectionMeta

from .votes import VotesSerializer, VotesTableSerializer


class FlattenMixin:
    """
    Flatens the specified related objects in this representation.

    Borrowing this clever method from:
    https://stackoverflow.com/a/41418576/1961614
    """
    def to_representation(self, obj):
        assert hasattr(self.Meta, 'flatten'), (
            'Class {serializer_class} missing "Meta.flatten" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        # Get the current object representation
        rep = super(FlattenMixin, self).to_representation(obj)
        # Iterate the specified related objects with their serializer
        for field, serializer_class in self.Meta.flatten:
            try:
                serializer = serializer_class(context=self.context)
                objrep = serializer.to_representation(getattr(obj, field))
                # Include their fields, prefixed, in the current representation
                for key in objrep:
                    rep[key] = objrep[key]
            except Exception:
                continue
        return rep


class DivisionSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_level(self, obj):
        """DivisionLevel slug"""
        return obj.level.slug

    def get_code(self, obj):
        if obj.level.name == 'state':
            return us.states.lookup(obj.code).abbr
        return obj.code

    class Meta:
        model = Division
        fields = (
            'code',
            'level'
        )


class PersonSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        """Object of images serialized by tag name."""
        return {str(i.tag): i.image.url for i in obj.images.all()}

    class Meta:
        model = Person
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'suffix',
            'images',
        )


class CandidateSerializer(FlattenMixin, serializers.ModelSerializer):
    party = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

    def get_party(self, obj):
        """Party AP code."""
        return obj.party.ap_code

    def get_order(self, obj):
        return obj.color_order.order

    class Meta:
        model = Candidate
        fields = (
            'party',
            'ap_candidate_id',
            'incumbent',
            'uid',
            'order',
        )
        flatten = (
            ('person', PersonSerializer),
        )


class CandidateElectionSerializer(FlattenMixin, serializers.ModelSerializer):
    override_winner = serializers.SerializerMethodField()
    override_runoff = serializers.SerializerMethodField()

    def get_override_winner(self, obj):
        """Winner marked in backend."""
        if obj.election.division.level.name == DivisionLevel.DISTRICT:
            division = obj.election.division.parent
        else:
            division = obj.election.division

        vote = obj.votes.filter(division=division).first()
        return vote.winning if vote else False

    def get_override_runoff(self, obj):
        if obj.election.division.level.name == DivisionLevel.DISTRICT:
            division = obj.election.division.parent
        else:
            division = obj.election.division

        vote = obj.votes.filter(division=division).first()
        return vote.runoff if vote else False

    class Meta:
        model = CandidateElection
        fields = (
            'aggregable',
            'uncontested',
            'override_winner',
            'override_runoff',
        )
        flatten = (
            ('candidate', CandidateSerializer),
        )


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = (
            'uid',
            'slug',
            'name',
            'label',
            'short_label',
        )


class APElectionMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = APElectionMeta
        fields = (
            'ap_election_id',
            'called',
            'tabulated',
            'override_ap_call',
            'override_ap_votes',
        )


class ElectionSerializer(FlattenMixin, serializers.ModelSerializer):
    primary = serializers.SerializerMethodField()
    primary_party = serializers.SerializerMethodField()
    runoff = serializers.SerializerMethodField()
    special = serializers.SerializerMethodField()
    office = serializers.SerializerMethodField()
    candidates = CandidateSerializer(many=True, read_only=True)
    date = serializers.SerializerMethodField()
    division = DivisionSerializer()
    candidates = serializers.SerializerMethodField()
    override_votes = serializers.SerializerMethodField()

    def get_override_votes(self, obj):
        """
        Votes entered into backend.
        Only used if ``override_ap_votes = True``.
        """
        if hasattr(obj, 'meta'):  # TODO: REVISIT THIS
            if obj.meta.override_ap_votes:
                all_votes = None
                for ce in obj.candidate_elections.all():
                    if all_votes:
                        all_votes = all_votes | ce.votes.all()
                    else:
                        all_votes = ce.votes.all()
                return VotesSerializer(all_votes, many=True).data
        return False

    def get_candidates(self, obj):
        """
        CandidateElections.
        """
        return CandidateElectionSerializer(
            obj.candidate_elections.all(),
            many=True
        ).data

    def get_primary(self, obj):
        """
        If primary
        """
        return obj.election_type.is_primary()

    def get_primary_party(self, obj):
        """
        If primary, party AP code.
        """
        if obj.party:
            return obj.party.ap_code
        return None

    def get_runoff(self, obj):
        """
        If runoff
        """
        return obj.election_type.is_runoff()

    def get_special(self, obj):
        """
        If special
        """
        return obj.race.special

    def get_office(self, obj):
        """Office candidates are running for."""
        return OfficeSerializer(obj.race.office).data

    def get_date(self, obj):
        """Election date."""
        return obj.election_day.date

    class Meta:
        model = Election
        fields = (
            'uid',
            'date',
            'office',
            'primary',
            'primary_party',
            'runoff',
            'special',
            'division',
            'candidates',
            'override_votes'
        )
        flatten = (
            ('meta', APElectionMetaSerializer),
        )


class ElectionViewSerializer(ElectionSerializer):
    """
    Serializes the election for passing into template view context.
    We split these because we have data in here we don't want to reach
    the deployed JSON.
    """

    votes_table = serializers.SerializerMethodField()

    def get_primary_party(self, obj):
        """
        If primary, party label.
        """
        if obj.party:
            return obj.party.label
        return None

    def get_votes_table(self, obj):
        if hasattr(obj, 'meta'):
            all_votes = None
            for ce in obj.candidate_elections.all():
                if all_votes:
                    all_votes = all_votes | ce.votes.filter(
                        division__level__name=DivisionLevel.STATE
                    )
                else:
                    all_votes = ce.votes.filter(
                        division__level__name=DivisionLevel.STATE
                    )
            return VotesTableSerializer(all_votes, many=True).data
        return False

    class Meta:
        model = Election
        fields = (
            'uid',
            'date',
            'office',
            'primary',
            'primary_party',
            'runoff',
            'special',
            'division',
            'candidates',
            'override_votes',
            'votes_table'
        )
        flatten = (
            ('meta', APElectionMetaSerializer),
        )
