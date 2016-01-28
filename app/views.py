from django.http import JsonResponse
from django.utils import timezone
from django.views.generic.base import View

from .models import Service


class SpotligthView(View):
    def get(self, request, *args, **kwargs):
        obj = Service.objects.all().order_by('?').first()

        return JsonResponse({
            'title': (obj.end_date - timezone.now().date()).days,
            'title_label': 'DAYS TO GO',
            'text_1': obj.customer_name,
            'text_1_label': 'CUSTOMER',
            'text_2': obj.website,
            'text_2_label': 'WEBSITE',
            'text_3': obj.get_type_display(),
            'text_3_label': 'SERVICE',
        })
