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

    def __str__(self):
        return u'{0}'.format(self.customer_name)

    @property
    def days_to_go(self):
        from django.utils import timezone
        return (self.end_date - timezone.now().date()).days

    @property
    def website_display(self):
        from urllib.parse import urlsplit
        return '{0.netloc}'.format(urlsplit(self.website))


class GoogleAnalyticsSite(models.Model):
    website = models.URLField()

    ga_view_id = models.PositiveSmallIntegerField()

    def __str__(self):
        return u'{0}'.format(self.website)


class GoogleAnalyticsSiteGoal(models.Model):
    name = models.CharField(
        max_length=20,
    )

    website = models.URLField()

    ga_metric_id = models.CharField(
        max_length=10,
    )

    def __str__(self):
        return u'{0}'.format(self.name)
