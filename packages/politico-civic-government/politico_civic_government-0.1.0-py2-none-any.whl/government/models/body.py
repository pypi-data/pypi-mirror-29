import uuid

from django.db import models
from entity.models import Organization
from government.constants import STOPWORDS
from uuslug import slugify, uuslug


class Body(models.Model):
    """
    A body represents a collection of offices or individuals organized around a
    common government or public service function.

    For example: the U.S. Senate, Florida House of Representatives, Columbia
    City Council, etc.

    .. note::
        Duplicate slugs are allowed on this model to accomodate states, for
        example:

        - florida/senate/
        - michigan/senate/
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(
        max_length=500,
        editable=False,
        blank=True)

    slug = models.SlugField(
        blank=True, max_length=255, editable=True,
        help_text="Customizable slug. Defaults to Org slug without stopwords.")
    label = models.CharField(max_length=255, blank=True)
    short_label = models.CharField(max_length=50, null=True, blank=True)

    organization = models.OneToOneField(
        Organization, related_name='government_body', on_delete=models.PROTECT)
    jurisdiction = models.ForeignKey('Jurisdiction', on_delete=models.PROTECT)

    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Bodies"

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`{jurisdiction.uid}_body:{slug}`
        """
        stripped_name = ' '.join(
            w for w in self.organization.name.split()
            if w not in STOPWORDS
        )

        if not self.slug:
            self.slug = uuslug(
                stripped_name,
                instance=self,
                max_length=100,
                separator='-',
                start_no=2
            )
        self.uid = '{}_body:{}'.format(
            self.jurisdiction.uid, slugify(stripped_name))

        super(Body, self).save(*args, **kwargs)
