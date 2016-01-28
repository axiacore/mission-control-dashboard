from django.db import models


class Service(models.Model):
    TYPE_CHOICES = (
        (10, 'Mission Control'),
        (20, 'SSL Certificate'),
        (30, 'Infrastructure'),
    )

    start_date = models.DateField()

    end_date = models.DateField()

    customer_name = models.CharField(
        max_length=20,
    )

    invoice_number = models.CharField(
        max_length=10,
    )

    website = models.URLField()

    type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
    )

    def __unicode__(self):
        return u'{0}'.format(self.identifier)

    class Meta:
        ordering = ['id']
