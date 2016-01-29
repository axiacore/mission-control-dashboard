from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.base import View

from .models import Service

import requests


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'


class SpotligthView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = Service.objects.all().order_by('?').first()
        if not obj:
            raise Http404('Create a service first')

        return JsonResponse({
            'title': (obj.end_date - timezone.now().date()).days,
            'title_label': 'DAYS TO GO',
            'text_1': obj.customer_name,
            'text_1_label': 'CUSTOMER',
            'text_2': '{0.netloc}'.format(urlsplit(obj.website)),
            'text_2_label': 'WEBSITE',
            'text_3': obj.get_type_display(),
            'text_3_label': 'SERVICE',
        })


class TickerView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = []

        # Zendesk
        req = requests.get(
            settings.ZENDESK_URL,
            auth=(settings.ZENDESK_EMAIL, settings.ZENDESK_API),
        )
        if req.ok:
            response.append({
                'title': 'Tickets',
                'label': 'Zendesk',
                'value': req.json()['view_count']['value'],
            })

        # Sentry
        req = requests.get(settings.SENTRY_URL, auth=(settings.SENTRY_KEY, ''))
        if req.ok:
            response.append({
                'title': 'Events',
                'label': 'Sentry',
                'value': sum([x[1] for x in req.json()]),
            })

        return JsonResponse({
            'list': response,
        })
