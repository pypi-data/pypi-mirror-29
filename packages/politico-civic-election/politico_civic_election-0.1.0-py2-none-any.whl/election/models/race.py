from django.db import models
from government.models import Office
from uuslug import uuslug


class Race(models.Model):
    """
    A race for an office comprised of one or many elections.
    """
    uid = models.CharField(
        max_length=500,
        primary_key=True,
        editable=False,
        blank=True
    )

    slug = models.SlugField(
        blank=True, max_length=255, unique=True, editable=False)

    label = models.CharField(max_length=255, blank=True)
    short_label = models.CharField(max_length=50, null=True, blank=True)

    office = models.ForeignKey(
        Office, related_name='races', on_delete=models.PROTECT)
    cycle = models.ForeignKey(
        'ElectionCycle', related_name='races', on_delete=models.PROTECT)
    special = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`{office.uid}_{cycle.uid}_race`
        """
        self.uid = '{}_{}_race'.format(
            self.office.uid,
            self.cycle.uid
        )

        name_label = '{0} {1}'.format(
            self.cycle.name,
            self.office.label
        )

        if self.special:
            self.uid = '{}:special'.format(
                self.uid
            )
            name_label = '{} Special'.format(
                name_label
            )

        self.label = name_label
        self.name = name_label
        if not self.slug:
            self.slug = uuslug(
                name_label,
                instance=self,
                max_length=100,
                separator='-',
                start_no=2
            )

        super(Race, self).save(*args, **kwargs)
