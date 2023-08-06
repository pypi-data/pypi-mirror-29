import os
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from election.models import ElectionDay
from geography.models import Division, DivisionLevel

from electionnight.managers.page_content import PageContentManager

from .page_type import PageType


class PageContent(models.Model):
    """
    A specific page that content can attach to.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    allowed_types = models.Q(app_label='geography', model='division') | \
        models.Q(app_label='government', model='office') | \
        models.Q(app_label='government', model='body') | \
        models.Q(app_label='electionnight', model='pagetype')
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=allowed_types,
        on_delete=models.CASCADE
    )
    object_id = models.CharField(max_length=500)
    content_object = GenericForeignKey('content_type', 'object_id')

    election_day = models.ForeignKey(ElectionDay, on_delete=models.PROTECT)

    division = models.ForeignKey(
        Division, null=True, blank=True, on_delete=models.PROTECT)

    special_election = models.BooleanField(default=False)

    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.PROTECT)

    objects = PageContentManager()

    class Meta:
        unique_together = (
            'content_type',
            'object_id',
            'election_day',
            'division'
        )

    def __str__(self):
        return self.page_location()

    def page_location(self):
        """
        Returns the published URL for page.
        """
        cycle = self.election_day.cycle.name
        if self.content_type.model_class() == PageType:
            return self.content_object.page_location_template()
        elif self.content_type.model_class() == Division:
            if self.content_object.level.name == DivisionLevel.STATE:
                if self.special_election:
                    # /{state}/special-election/{month-day}/
                    path = os.path.join(
                        self.content_object.slug,
                        'special-election',
                        self.election_day.special_election_datestring()
                    )
                else:
                    # /{state}/
                    path = self.content_object.slug
            else:
                # /  National
                path = ''
        # Offices and Bodies
        else:
            if self.division.level.name == DivisionLevel.STATE:
                path = os.path.join(
                    self.division.slug, self.content_object.slug)
            else:
                path = self.content_object.slug
        return os.sep + os.path.normpath(
            os.path.join(cycle, path)
        ) + os.sep  # normalized URL
