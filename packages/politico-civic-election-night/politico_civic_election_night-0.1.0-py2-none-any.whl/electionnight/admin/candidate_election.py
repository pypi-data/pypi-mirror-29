from django.contrib import admin


class CandidateElectionAdmin(admin.ModelAdmin):
    list_display = (
        'candidate_name',
        'party',
        'election',
    )
    ordering = (
        'election',
        'election__division__label',
        'candidate__person__last_name'
    )

    def candidate_name(self, obj):
        return obj.candidate.person.full_name

    def party(self, obj):
        return obj.candidate.party
