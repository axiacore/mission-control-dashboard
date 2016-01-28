from django.contrib import admin

from .models import Service


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
