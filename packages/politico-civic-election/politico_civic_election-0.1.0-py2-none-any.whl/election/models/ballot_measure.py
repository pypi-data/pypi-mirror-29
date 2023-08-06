from django.db import models
from geography.models import Division


class BallotMeasure(models.Model):
    """A ballot measure."""
    uid = models.CharField(
        max_length=500,
        primary_key=True,
        editable=False,
        blank=True
    )

    label = models.CharField(max_length=255, blank=True)
    short_label = models.CharField(max_length=50, null=True, blank=True)

    question = models.TextField()
    division = models.ForeignKey(
        Division, related_name='ballot_measures', on_delete=models.PROTECT)
    number = models.CharField(max_length=3)
    election_day = models.ForeignKey(
        'ElectionDay', related_name='ballot_measures',
        on_delete=models.PROTECT)

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`division_cycle_ballotmeasure:{number}`
        """
        self.uid = '{}_{}_ballotmeasure:{}'.format(
            self.division.uid,
            self.election_day.uid,
            self.number
        )
        super(BallotMeasure, self).save(*args, **kwargs)
