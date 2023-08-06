import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import models
from election.models import ElectionDay
from geography.models import Division, DivisionLevel
from government.models import Body, Jurisdiction, Office


class PageType(models.Model):
    """
    A type of page that content can attach to.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    allowed_types = models.Q(app_label='geography', model='division') | \
        models.Q(app_label='entity', model='office') | \
        models.Q(app_label='entity', model='body')
    model_type = models.ForeignKey(
        ContentType,
        limit_choices_to=allowed_types,
        on_delete=models.CASCADE
    )
    election_day = models.ForeignKey(ElectionDay, on_delete=models.CASCADE)
    division_level = models.ForeignKey(DivisionLevel, on_delete=models.CASCADE)
    jurisdiction = models.ForeignKey(
        Jurisdiction, on_delete=models.CASCADE, blank=True, null=True,
        help_text='Only set jurisdiction for federal pages')
    body = models.ForeignKey(
        Body, on_delete=models.CASCADE, blank=True, null=True,
        help_text='Only set body for senate/house pages')
    office = models.ForeignKey(
        Office, on_delete=models.CASCADE, blank=True, null=True,
        help_text='Only set office for the presidency')

    class Meta:
        unique_together = (
            'model_type',
            'election_day',
            'division_level',
            'jurisdiction',
            'body',
            'office'
        )

    def __str__(self):
        return self.page_location_template()

    def page_location_template(self):
        """
        Returns the published URL template for a page type.
        """
        cycle = self.election_day.cycle.name
        model_class = self.model_type.model_class()
        if model_class == Office:
            # President
            if self.jurisdiction:
                if self.division_level.name == DivisionLevel.STATE:
                    return '/{}/president/{{state}}'.format(cycle)
                else:
                    return '/{}/president/'.format(cycle)
            # Governor
            else:
                return '/{}/{{state}}/governor/'.format(cycle)
        elif model_class == Body:
            # Senate
            if self.body.name == 'senate':
                if self.jurisdiction:
                    if self.division_level.name == DivisionLevel.STATE:
                        return '/{}/senate/{{state}}/'.format(cycle)
                    else:
                        return '/{}/senate/'.format(cycle)
                else:
                    return '/{}/{{state}}/senate/'.format(cycle)
            # House
            else:
                if self.jurisdiction:
                    if self.division_level.name == DivisionLevel.STATE:
                        return '/{}/house/{{state}}/'.format(cycle)
                    else:
                        return '/{}/house/'.format(cycle)
                else:
                    return '/{}/{{state}}/house/'.format(cycle)
        elif model_class == Division:
            return '/{}/{{state}}/'.format(cycle)
        else:
            return 'ORPHAN TYPE'
