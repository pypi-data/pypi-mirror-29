import uuid

from django.db import models


class CandidateElection(models.Model):
    """
    A CandidateElection represents the abstract relationship between a
    candidate and an election and carries properties like whether the
    candidate is uncontested or whether we aggregate their vote totals.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(
        'Candidate',
        on_delete=models.CASCADE,
        related_name='candidate_elections'
    )
    election = models.ForeignKey(
        'Election',
        on_delete=models.CASCADE,
        related_name='candidate_elections'
    )
    aggregable = models.BooleanField(default=True)
    uncontested = models.BooleanField(default=False)

    class Meta:
        unique_together = (('candidate', 'election'),)
