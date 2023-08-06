from django.contrib import admin


class CandidateColorOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'race', 'party', 'order')
    list_editable = ('order',)
    ordering = (
        'candidate__race__office__division__code',
        'candidate__race',
        'candidate__party',
        'order'
    )

    def name(self, obj):
        return obj.candidate.person.full_name

    def party(self, obj):
        return obj.candidate.party

    def race(self, obj):
        return obj.candidate.race
