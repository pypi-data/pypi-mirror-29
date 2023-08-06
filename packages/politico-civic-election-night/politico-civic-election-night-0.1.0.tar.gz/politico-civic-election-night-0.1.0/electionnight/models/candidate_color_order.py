from django.db import models
from election.models import Candidate


class CandidateColorOrder(models.Model):
    """
    Determines the color ordering of candidates for maps
    """
    candidate = models.OneToOneField(
        Candidate,
        related_name='color_order',
        on_delete=models.CASCADE,
        unique=True
    )
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{0} {1}'.format(
            self.candidate.person.last_name,
            self.candidate.race.label
        )