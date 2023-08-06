from django.contrib import admin


class VotesAdmin(admin.ModelAdmin):
    list_display = (
        'candidate',
        'party',
        'election',
        'division',
        'count',
        'pct',
        'winning',
        'runoff'
    )
    list_editable = ('count', 'pct', 'winning', 'runoff')
    ordering = (
        'candidate_election__election',
        'division__label',
        'candidate_election__candidate__person__last_name'
    )

    def candidate(self, obj):
        return obj.candidate_election.candidate.person.full_name

    def party(self, obj):
        return obj.candidate_election.candidate.party

    def election(self, obj):
        return obj.candidate_election.election

    def division(self, obj):
        return obj.division
