from django.contrib import admin

from .models import Service
from .models import GoogleAnalyticsSite
from .models import GoogleAnalyticsSiteGoal


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type',
        'start_date',
        'end_date',
        'customer_name',
        'invoice_number',
        'website',
    ]

    list_filter = [
        'type',
    ]


@admin.register(GoogleAnalyticsSite)
class GoogleAnalyticsSiteAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'website',
        'ga_view_id',
    ]


@admin.register(GoogleAnalyticsSiteGoal)
class GoogleAnalyticsSiteGoalAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'website',
        'ga_metric_id',
    ]

    list_filter = [
        'website',
    ]
