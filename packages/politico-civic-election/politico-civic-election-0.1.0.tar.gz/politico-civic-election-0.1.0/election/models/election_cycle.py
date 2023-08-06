from django.db import models
from uuslug import slugify


class ElectionCycle(models.Model):
    uid = models.CharField(
        max_length=10,
        primary_key=True,
        editable=False,
        blank=True
    )
    slug = models.SlugField(
        blank=True, max_length=4, unique=True, editable=False
    )
    name = models.CharField(max_length=4)

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`cycle:{year}`
        """
        self.slug = slugify(self.name)
        self.uid = 'cycle:{}'.format(self.slug)
        super(ElectionCycle, self).save(*args, **kwargs)
