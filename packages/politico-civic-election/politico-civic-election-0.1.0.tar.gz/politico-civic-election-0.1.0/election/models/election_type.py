from django.db import models


class ElectionType(models.Model):
    """
    e.g., "General", "Primary"
    """
    GENERAL = 'general'
    PARTY_PRIMARY = 'party-primary'
    JUNGLE_PRIMARY = 'jungle-primary'
    PRIMARY_RUNOFF = 'primary-runoff'
    GENERAL_RUNOFF = 'general-runoff'

    TYPES = (
        (GENERAL, 'General'),
        (PARTY_PRIMARY, 'Party Primary'),
        (JUNGLE_PRIMARY, 'Jungle Primary'),
        (PRIMARY_RUNOFF, 'Primary Runoff'),
        (GENERAL_RUNOFF, 'General Runoff')
    )

    uid = models.CharField(
        max_length=500,
        primary_key=True,
        editable=False,
        blank=True)

    slug = models.SlugField(
        blank=True, max_length=255, unique=True, choices=TYPES
    )
    label = models.CharField(max_length=255, blank=True)
    short_label = models.CharField(max_length=50, null=True, blank=True)

    ap_code = models.CharField(max_length=1, null=True, blank=True)
    number_of_winners = models.PositiveSmallIntegerField(default=1)
    winning_threshold = models.DecimalField(
        decimal_places=3, max_digits=5, null=True, blank=True)

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`electiontype:{name}`
        """
        self.uid = 'electiontype:{}'.format(self.slug)
        super(ElectionType, self).save(*args, **kwargs)

    def is_primary(self):
        if self.slug in [self.PARTY_PRIMARY, self.JUNGLE_PRIMARY]:
            return True
        else:
            return False

    def is_runoff(self):
        if self.slug in [self.PRIMARY_RUNOFF, self.GENERAL_RUNOFF]:
            return True
        else:
            return False
