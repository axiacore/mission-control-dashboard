from itertools import cycle

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View

from .google_analytics import get_access_token
from .models import Service
from .models import GoogleAnalyticsSite
from .models import GoogleAnalyticsSiteGoal

import requests
from requests.exceptions import ConnectionError


spotligth_cycle = cycle('AB')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class SpotligthView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        case = next(spotligth_cycle)
        if case == 'A':
            obj = Service.objects.all().order_by('?').first()
            if not obj:
                raise Http404('Create a Service first')

            return render(request, 'service_detail.html', {
                'obj': obj,
            })

        elif case == 'B':
            obj = GoogleAnalyticsSite.objects.all().order_by('?').first()
            if not obj:
                raise Http404('Create a GoogleAnalyticsSite first')

            return render(request, 'googleanalyticssite_detail.html', {
                'ACCESS_TOKEN': get_access_token(),
                'obj': obj,
            })


class TickerView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response_list = []

        # Zendesk
        zendesk_data = cache.get('zendesk_data')
        if not zendesk_data:
            try:
                req = requests.get(
                    settings.ZENDESK_URL,
                    auth=(settings.ZENDESK_EMAIL, settings.ZENDESK_API),
                )
                if req.ok:
                    zendesk_data = {
                        'title': 'Tickets',
                        'label': 'Zendesk',
                        'value': req.json()['view_count']['value'],
                    }
                    cache.set('zendesk_data', zendesk_data, 120)
            except ConnectionError:
                zendesk_data = None

        if zendesk_data:
            response_list.append(zendesk_data)

        # Sentry
        sentry_data = cache.get('sentry_data')
        if not sentry_data:
            try:
                req = requests.get(
                    settings.SENTRY_URL,
                    auth=(settings.SENTRY_KEY, ''),
                )
                if req.ok:
                    sentry_data = {
                        'title': 'Events',
                        'label': 'Sentry',
                        'value': sum([x[1] for x in req.json()]),
                    }
                    cache.set('sentry_data', sentry_data, 60)
            except ConnectionError:
                sentry_data = None

        if sentry_data:
            response_list.append(sentry_data)

        # Mmonit
        mmonit_list = cache.get('mmonit_list')
        if not mmonit_list:
            try:
                s = requests.Session()
                s.get(settings.MMONIT_URL + 'index.csp')
                s.post(
                    settings.MMONIT_URL + 'z_security_check',
                    params={
                        'z_username': settings.MMONIT_USER,
                        'z_password': settings.MMONIT_PASS,
                    }
                )
                req = s.post(
                    settings.MMONIT_URL + 'reports/uptime/list',
                    params={'range': '6'},
                )
                if req.ok:
                    mmonit_list = []
                    for item in req.json()['items']:
                        mmonit_list.append({
                            'title': item['name'],
                            'label': 'Uptime',
                            'value': '{0}%'.format(item['uptime']),
                        })
                    cache.set('mmonit_list', mmonit_list, 90)
            except ConnectionError:
                mmonit_list = None

        if mmonit_list:
            response_list += mmonit_list

        return render(request, 'ticker_detail.html', {
            'response_list': response_list,
        })
