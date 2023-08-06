from django import forms
from django.contrib import admin

from electionnight.models import PageContentBlock


class BlockAdminForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorWidget()) # TODO: To markdown

    class Meta:
        model = PageContentBlock
        fields = (
            'content_type',
            'content',
        )


class PageContentBlockInline(admin.StackedInline):
    model = PageContentBlock
    extra = 0
    form = BlockAdminForm


class PageContentAdmin(admin.ModelAdmin):
    inlines = [
        PageContentBlockInline
    ]
    list_filter = ('election_day', 'content_type',)
    list_display = ('page_location', 'election_day',)
    search_fields = ('page_location',)
    # actions = None
    readonly_fields = (
        'election_day',
        'page_location',
        'content_object',
        'division',
    )
    fieldsets = (
        (None, {
            'fields': ('page_location',),
        }),
        ('Page Meta', {
            'fields': (
                'election_day',
                'content_object',
                'division',
            ),
        }),
    )
