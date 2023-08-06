import uuid

from django.db import models
from geography.models import Division
from government.constants import STOPWORDS
from uuslug import slugify, uuslug


class Jurisdiction(models.Model):
    """
    A Jurisdiction represents a logical unit of governance, comprised of
    a collection of legislative bodies, administrative offices or public
    services.

    For example: the United States Federal Government, the Government
    of the District of Columbia, Columbia Missouri City Government, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(
        max_length=500,
        editable=False,
        blank=True)

    slug = models.SlugField(
        blank=True, max_length=255, unique=True, editable=False)
    name = models.CharField(max_length=255)

    division = models.ForeignKey(Division, null=True, on_delete=models.PROTECT)

    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`{division.uid}_jurisdiction:{slug}`
        """
        stripped_name = ' '.join(
            w for w in self.name.split()
            if w not in STOPWORDS
        )

        self.slug = uuslug(
            stripped_name,
            instance=self,
            max_length=100,
            separator='-',
            start_no=2
        )
        self.uid = '{}_jurisdiction:{}'.format(
            self.division.uid, slugify(stripped_name))

        super(Jurisdiction, self).save(*args, **kwargs)
