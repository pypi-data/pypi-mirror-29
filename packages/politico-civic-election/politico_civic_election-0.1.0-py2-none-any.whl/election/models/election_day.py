from django.db import models


class ElectionDay(models.Model):
    """
    A day on which one or many elections can be held.
    """
    uid = models.CharField(
        max_length=500,
        primary_key=True,
        editable=False,
        blank=True
    )

    slug = models.SlugField(
        blank=True, max_length=255, unique=True, editable=False
    )

    date = models.DateField(unique=True)
    cycle = models.ForeignKey(
        'ElectionCycle', related_name='elections_days',
        on_delete=models.PROTECT)

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`{cycle.uid}_date:{date}`
        """
        self.uid = '{}_date:{}'.format(
            self.cycle.uid,
            self.date
        )
        self.slug = '{}'.format(self.date)
        super(ElectionDay, self).save(*args, **kwargs)

    def special_election_datestring(self):
        """
        Formatted date string used in URL for special elections.
        """
        return self.date.strftime('%b-%d').lower()
