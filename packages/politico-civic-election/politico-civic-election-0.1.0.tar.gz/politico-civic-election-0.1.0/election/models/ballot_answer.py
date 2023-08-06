import uuid

from django.db import models


class BallotAnswer(models.Model):
    """An answer to a ballot question."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    label = models.CharField(max_length=255, blank=True)
    short_label = models.CharField(max_length=50, null=True, blank=True)

    answer = models.TextField()
    winner = models.BooleanField(default=False)
    ballot_measure = models.ForeignKey(
        'BallotMeasure', on_delete=models.CASCADE)
