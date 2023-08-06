import uuid

from django.db import models
from entity.models import Organization
from uuslug import slugify


class Party(models.Model):
    """
    A political party.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(
        max_length=500,
        editable=False,
        blank=True)
    slug = models.SlugField(
        blank=True, max_length=255, editable=True,
        help_text="Customizable slug. Defaults to slugged Org name.")
    label = models.CharField(max_length=255, blank=True)
    short_label = models.CharField(max_length=50, null=True, blank=True)

    organization = models.OneToOneField(
        Organization, related_name='political_party', on_delete=models.PROTECT,
        blank=True, null=True,
        help_text="All parties except Independent should attach to an Org.")

    ap_code = models.CharField(max_length=3, unique=True)
    aggregate_candidates = models.BooleanField(
        default=True,
        help_text="Determines whether to globally aggregate vote totals of this \
        party's candidates during an election."
    )

    def __str__(self):
        if self.label:
            return self.label
        return self.uid

    class Meta:
        verbose_name_plural = 'Parties'

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`party:{apcode}`
        """
        self.uid = 'party:{}'.format(slugify(self.ap_code))
        if not self.slug:
            if self.organization:
                self.slug = slugify(self.organization.name)
            else:
                self.slug = slugify(self.label)
        super(Party, self).save(*args, **kwargs)
